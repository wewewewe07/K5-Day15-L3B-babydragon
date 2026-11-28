"""Chạy bộ test chịu tải (tests/stress_cases.csv) và/hoặc bộ benchmark chính thức để kiểm hồi quy.

Không ghi file run-N của khung, không đụng eval/. Kết quả in ra màn hình + ghi tests/last_stress_result.csv.

    python tests/run_stress.py            # chỉ bộ stress
    python tests/run_stress.py --bench    # chỉ benchmark (24 câu) — kiểm hồi quy
    python tests/run_stress.py --all      # cả hai
    python tests/run_stress.py --only S05,S11
"""
import csv
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "codebase"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tracing  # noqa: E402
from agent import answer  # noqa: E402

LABELS = ("KHOP_NGUON", "SAI_MAU_THUAN", "LOI_CAU_HOI", "THIEU_NGUON", "TU_CHOI")

VALID = {x["code"].upper() for x in json.load(open(os.path.join(ROOT, "data", "course_sources.json"), encoding="utf-8-sig"))}


def load_stress():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "tests", "stress_cases.csv"), encoding="utf-8-sig")))
    return [{"id": r["id"], "cat": r["category"], "input": r["input"],
             "accept": set(r["accept"].split("|")), "cite": [c for c in r["must_cite"].split("|") if c]} for r in rows]


def load_bench():
    out = []
    for r in csv.DictReader(open(os.path.join(ROOT, "eval", "benchmark.csv"), encoding="utf-8-sig")):
        exp = r["expected"].strip()
        label = exp.split()[0]
        accept = {label}
        crit = r["pass_criterion"]
        for alt in LABELS:  # pass_criterion có ghi "(hoặc X)" thì chấp nhận X
            if re.search(r"hoặc\s+%s" % alt, crit):
                accept.add(alt)
        cite = re.findall(r"SRC-D\d{2}-M\d-\d{2}", exp)
        out.append({"id": r["id"], "cat": "bench_" + r["type"], "input": r["input"], "accept": accept,
                    "cite": cite if label in ("KHOP_NGUON", "SAI_MAU_THUAN", "LOI_CAU_HOI") else []})
    return out


def grade(case, output):
    first = (output.strip().splitlines() or [""])[0]
    m = re.match(r"\W*([A-Z_]+)", first)
    label = m.group(1) if m else ""
    cited = {c.upper() for c in re.findall(r"SRC-[A-Z0-9]+(?:-[A-Z0-9]+)*", output, flags=re.I)}
    fake = sorted(c for c in cited if c not in VALID)
    problems = []
    if label not in case["accept"]:
        problems.append("nhãn %s, cần %s" % (label or "?", "/".join(sorted(case["accept"]))))
    if fake:
        problems.append("có mã giả trong output: " + ", ".join(fake))
    if label in ("KHOP_NGUON", "SAI_MAU_THUAN", "LOI_CAU_HOI"):
        for c in case["cite"]:
            if c.upper() not in cited:
                problems.append("thiếu mã " + c)
    return label, problems


def main(argv):
    cases = []
    if "--bench" in argv or "--all" in argv:
        cases += load_bench()
    if "--bench" not in argv or "--all" in argv:
        cases += load_stress()
    if "--only" in argv:
        keep = set(argv[argv.index("--only") + 1].split(","))
        cases = [c for c in cases if c["id"] in keep]
    results, n_ok, tok_in, tok_out = [], 0, 0, 0
    t0 = time.time()
    for c in cases:
        tracing.begin(c["id"])
        err = ""
        try:
            out = answer(c["input"])["output"]
        except Exception as e:  # noqa: BLE001
            out, err = "", "%s: %s" % (type(e).__name__, e)
        s, _ = tracing.end()
        tok_in += s["tokens_in"]
        tok_out += s["tokens_out"]
        label, probs = grade(c, out)
        if err:
            probs.insert(0, "lỗi: " + err)
        ok = not probs
        n_ok += ok
        print("%s %-4s %-18s %-14s %s" % ("✅" if ok else "❌", c["id"], c["cat"], label, "; ".join(probs)))
        results.append({"id": c["id"], "category": c["cat"], "label": label, "ok": int(ok),
                        "problems": "; ".join(probs), "model_calls": s["model_calls"],
                        "tokens_in": s["tokens_in"], "tokens_out": s["tokens_out"], "output": out})
    print("\nĐạt %d/%d · token vào %d · ra %d · %.0f giây" % (n_ok, len(cases), tok_in, tok_out, time.time() - t0))
    path = os.path.join(ROOT, "tests", "last_stress_result.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    print("Chi tiết: tests/last_stress_result.csv")


if __name__ == "__main__":
    main(sys.argv[1:])
