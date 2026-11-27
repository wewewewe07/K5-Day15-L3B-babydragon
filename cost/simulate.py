"""Mô phỏng chi phí khi dùng thật — KHUNG, nhóm không cần sửa. Nhóm điền cost/personas.yaml. Gọi qua run.py:

  python run.py simulate --try [N]    chạy thử N phiên (mặc định 10) để kiểm khung → cost/simulate-try.csv
  python run.py simulate              chạy đủ số phiên trong personas.yaml (≥50) → cost/simulate-N.csv
                                      + cost/simulate-N-summary.md + traces/simulate-N.jsonl
  python run.py simulate --wait 4     như trên, nghỉ 4 giây giữa hai lượt hỏi (gói miễn phí hay giới hạn lượt / phút)
  python run.py simulate --rate-from eval/run-2.csv
                                      lấy tỉ lệ đạt từ đúng lượt này (mặc định: lượt run-N mới nhất đã chấm, cùng model)

Cách tính (guide bước 4.2):
  1. Sinh các phiên theo persona (seed cố định): mỗi phiên chọn một persona theo tỉ lệ `share`,
     mỗi lượt hỏi lấy ngẫu nhiên một đầu vào (từ eval/benchmark.csv hoặc `inputs` của persona).
  2. Chạy THẬT từng lượt qua codebase/agent.py — token, số lần gọi model / công cụ đọc từ trace, không đoán.
  3. Chi phí mỗi phiên = token vào × giá vào + token ra × giá ra, cho từng model trong `prices`.
  4. Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt của lượt eval mới nhất đã chấm.
  5. Chi phí / tháng = Σ (số người dùng × share × số phiên / người / tháng × chi phí trung bình mỗi phiên của persona),
     cho 3 kịch bản số người dùng thấp · cơ sở · cao.

Chỉ dùng thư viện chuẩn.
"""
import datetime
import json
import math
import os
import random
import re
import sys
import time

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import run_eval as ev  # noqa: E402

PERSONAS = os.path.join(ROOT, "cost", "personas.yaml")
COST_DIR = os.path.join(ROOT, "cost")
TRY_DEFAULT = 10
SCENARIOS = ["low", "base", "high"]
SCENARIO_VI = {"low": "thấp", "base": "cơ sở", "high": "cao"}
DEFAULT_TYPES = ["thuong", "kho"]

USAGE = """Cách dùng:
  python run.py simulate --try [N]    chạy thử N phiên (mặc định 10) → cost/simulate-try.csv
  python run.py simulate              chạy đủ số phiên trong cost/personas.yaml → cost/simulate-N.csv + bản tóm tắt
  python run.py simulate --wait 4     nghỉ 4 giây giữa hai lượt hỏi
  python run.py simulate --rate-from eval/run-2.csv   lấy tỉ lệ đạt từ đúng lượt này"""


def fail(msg):
    sys.exit("cost/personas.yaml: " + msg)


def num(v, what, minimum=0.0):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v < minimum:
        fail("%s phải là số ≥%s (đang là %r)." % (what, minimum, v))
    return v


def load_config():
    if not os.path.exists(PERSONAS):
        sys.exit("Chưa có cost/personas.yaml — chép từ khung starter-repo và điền theo guide bước 4.2.")
    try:
        cfg = ev.load_yaml(PERSONAS)
    except ev.YamlError as e:
        fail(str(e))
    if not isinstance(cfg, dict):
        fail("cần các mục sessions, seed, users, personas, prices.")
    warn = []
    sessions = int(num(cfg.get("sessions", 50), "sessions", 1))
    seed = cfg.get("seed", 42)
    users = cfg.get("users") or {}
    if not isinstance(users, dict) or any(k not in users or users[k] is None for k in SCENARIOS):
        fail("users cần đủ low, base, high (số người dùng thật cho 3 kịch bản) + source.")
    for k in SCENARIOS:
        num(users[k], "users.%s" % k)
    if ev.placeholder(users.get("source")):
        warn.append("users.source trống — số người dùng phải có nguồn hoặc ghi rõ \"(tự ước tính)\".")
    personas = cfg.get("personas")
    if not isinstance(personas, list) or not personas:
        fail("personas cần ít nhất một persona (- name: …).")
    for k, p in enumerate(personas, start=1):
        if not isinstance(p, dict) or ev.placeholder(p.get("name")):
            fail("persona thứ %d cần name." % k)
        num(p.get("share"), "personas.%s.share" % p["name"])
        num(p.get("uses_per_month"), "personas.%s.uses_per_month" % p["name"])
        p["turns_per_session"] = int(num(p.get("turns_per_session", 1), "personas.%s.turns_per_session" % p["name"], 1))
        if ev.placeholder(p.get("source")):
            warn.append("persona %s: source trống — số lần dùng phải lấy từ data / phỏng vấn / khảo sát, hoặc ghi rõ \"(tự ước tính)\"." % p["name"])
    if len(personas) < 3:
        warn.append("Mới có %d persona — guide 4.2 cần ≥3 (dùng ít · vừa · nhiều)." % len(personas))
    total_share = sum(p["share"] for p in personas)
    if total_share <= 0:
        fail("tổng share của các persona phải > 0.")
    if abs(total_share - 1) > 0.01:
        warn.append("Tổng share = %.2f, không bằng 1 — khung chia lại theo tỉ lệ." % total_share)
    prices = cfg.get("prices")
    if not isinstance(prices, list) or not prices:
        fail("prices cần ít nhất một model (- model, input, output, source).")
    for k, pr in enumerate(prices, start=1):
        if not isinstance(pr, dict) or ev.placeholder(pr.get("model")):
            fail("giá thứ %d cần tên model." % k)
        num(pr.get("input"), "prices.%s.input" % pr["model"])
        num(pr.get("output"), "prices.%s.output" % pr["model"])
        if ev.placeholder(pr.get("source")):
            warn.append("Giá %s chưa có source (link + ngày xem)." % pr["model"])
    if len(prices) < 2:
        warn.append("Mới có giá của %d model — guide 4.2 cần ≥2 mức model (rẻ và mạnh)." % len(prices))
    fx = cfg.get("usd_to_vnd") if isinstance(cfg.get("usd_to_vnd"), dict) else {}
    rate = fx.get("rate") if isinstance(fx.get("rate"), (int, float)) and not isinstance(fx.get("rate"), bool) else None
    if "(ví dụ" in open(PERSONAS, encoding="utf-8-sig").read():
        warn.append("Còn chữ \"(ví dụ)\" trong cost/personas.yaml — thay bằng số và nguồn của nhóm.")
    return {"sessions": sessions, "seed": seed, "users": users, "personas": personas, "prices": prices,
            "fx_rate": rate, "fx_source": fx.get("source"), "total_share": total_share}, warn


def input_pool(persona, bench):
    if persona.get("inputs"):
        if not isinstance(persona["inputs"], list):
            fail("personas.%s.inputs phải là danh sách câu." % persona["name"])
        return [str(x) for x in persona["inputs"] if str(x or "").strip()]
    types = persona.get("types") or DEFAULT_TYPES
    pool = [r.get("input", "") for r in bench if r.get("type", "").strip() in types and r.get("input", "").strip()]
    if not pool:
        fail("persona %s không có đầu vào: eval/benchmark.csv không có câu type %s, và persona không có inputs."
             % (persona["name"], ", ".join(types)))
    return pool


def plan_sessions(cfg, bench, n_sessions):
    rng = random.Random(cfg["seed"])
    pools = {p["name"]: input_pool(p, bench) for p in cfg["personas"]}
    weights = [p["share"] for p in cfg["personas"]]
    plan = []
    for s in range(n_sessions):
        p = rng.choices(cfg["personas"], weights=weights)[0]
        plan.append(("S%03d" % (s + 1), p, [rng.choice(pools[p["name"]]) for _ in range(p["turns_per_session"])]))
    return plan


def money(usd, rate=None):
    if usd is None:
        return "—"
    if usd >= 1:
        text = "$" + format(usd, ",.2f")
    elif usd <= 0:
        text = "$0"
    else:  # số nhỏ: giữ 2 chữ số có nghĩa, không làm tròn về $0.0000
        decimals = max(4, 1 - math.floor(math.log10(usd)))
        text = "$%.*f" % (decimals, usd)
    return text + (" (≈ %s ₫)" % format(round(usd * rate), ",").replace(",", ".") if rate else "")


def measured_models(rows):
    """Các model thật sự được gọi trong những phiên không lỗi."""
    return sorted({m for r in rows if not r["error"] for m in r["model"].split(", ") if m})


def summarize(cfg, rows, graded, other=None):
    """→ danh sách dòng markdown của bản tóm tắt.
    graded: lượt eval đã chấm, chạy bằng ĐÚNG model đang mô phỏng (None nếu không có).
    other: lượt eval chấm xong gần nhất nhưng chạy bằng model khác — chỉ để cảnh báo, không dùng tính."""
    ok = [r for r in rows if not r["error"]]
    share = {p["name"]: p["share"] / cfg["total_share"] for p in cfg["personas"]}
    rate = graded["passed"] / graded["total"] if graded else None
    out = []
    out.append("| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |")
    out.append("|---|---:|---:|---:|---:|---:|---:|")
    per = {}
    for p in cfg["personas"]:
        s = [r for r in ok if r["persona"] == p["name"]]
        per[p["name"]] = s
        if s:
            avg = lambda k: sum(r[k] for r in s) / len(s)  # noqa: E731
            out.append("| %s | %d | %d | %.0f | %.0f | %.1f | %.1f |" % (p["name"], len(s), p["turns_per_session"],
                       avg("tokens_in"), avg("tokens_out"), avg("model_calls"), avg("tool_calls")))
        else:
            out.append("| %s | 0 | %d | — | — | — | — |" % (p["name"], p["turns_per_session"]))
    out.append("")
    if graded:
        rate_text = "%d/%d (%.0f%%) — lượt %s" % (graded["passed"], graded["total"], 100 * rate, graded["run_id"] or graded["name"])
    elif other:
        rate_text = ("**chưa có** lượt eval chấm xong chạy bằng %s. Lượt chấm gần nhất (%s) chạy bằng %s — model khác, "
                     "nên KHÔNG dùng tỉ lệ đạt đó → chưa tính chi phí / task thành công. Chạy `python run.py eval` bằng đúng "
                     "model này, chấm xong (`python run.py score …`) rồi chạy lại simulate."
                     % (", ".join(measured_models(rows)) or "model này", other["run_id"] or other["name"], ", ".join(other["models"]) or "?"))
    else:
        rate_text = "**chưa có** lượt eval nào chấm xong (`python run.py score eval/run-N.csv`) → chưa tính được chi phí / task thành công"
    out.append("Tỉ lệ đạt dùng để tính: %s" % rate_text)
    if graded and graded.get("why"):
        out.append("")
        out.append("- %s" % graded["why"])
    out.append("")
    measured = measured_models(rows)
    turns = sum(r["turns"] for r in ok) / len(ok) if ok else None
    head = "| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | " + " | ".join(
        "Chi phí / tháng — %s (%s người)" % (SCENARIO_VI[k], format(cfg["users"][k], ",").replace(",", ".")) for k in SCENARIOS) + \
        " | Chi phí / người / tháng (cơ sở) |"
    out.append(head)
    out.append("|---|" + "---:|" * (4 + len(SCENARIOS)))

    def table_row(label, cost):
        per_session = sum(cost(r) for r in ok) / len(ok) if ok else None
        per_task = per_session / rate if (per_session is not None and rate) else None
        per_q = per_session / turns / rate if (per_session is not None and rate and turns) else None
        persona_cost = {name: (sum(cost(r) for r in s) / len(s) if s else per_session) for name, s in per.items()}
        monthly = {}
        for k in SCENARIOS:
            monthly[k] = sum(cfg["users"][k] * share[p["name"]] * p["uses_per_month"] * (persona_cost[p["name"]] or 0)
                             for p in cfg["personas"])
        per_user = monthly["base"] / cfg["users"]["base"] if cfg["users"]["base"] else None
        out.append("| %s | %s | %s | %s | %s | %s |" % (
            label, money(per_session, cfg["fx_rate"]), money(per_task, cfg["fx_rate"]), money(per_q, cfg["fx_rate"]),
            " | ".join(money(monthly[k], cfg["fx_rate"]) for k in SCENARIOS), money(per_user, cfg["fx_rate"])))

    prices = {pr["model"].strip().lower(): pr for pr in cfg["prices"]}
    if len(measured) > 1:
        # Bản chạy thử gọi nhiều model: tính mỗi model theo token đo được của chính nó, giá của chính nó.
        missing = [m for m in measured if m.strip().lower() not in prices]
        if missing:
            out.append("| **Thực đo — mỗi model giá riêng** | chưa tính: thiếu giá của %s trong `prices` | — | — | %s — |"
                       % (", ".join(missing), "— | " * len(SCENARIOS)))
        else:
            def mixed(r):
                return sum((t["in"] * prices[m.strip().lower()]["input"] + t["out"] * prices[m.strip().lower()]["output"]) / 1e6
                           for m, t in r["by_model"].items())
            table_row("**Thực đo — mỗi model giá riêng** (%s)" % " + ".join(measured), mixed)
    for pr in cfg["prices"]:
        def cost(r, pr=pr):
            return (r["tokens_in"] * pr["input"] + r["tokens_out"] * pr["output"]) / 1e6
        label = "%s (vào %s · ra %s $/1M)" % (pr["model"], pr["input"], pr["output"])
        if len(measured) > 1:
            label += " — nếu MỌI token tính giá model này"
        table_row(label, cost)
    out.append("")
    out.append("- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi "
               "trung bình mỗi phiên (%s) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử." % ("%.1f" % turns if turns else "—"))
    out.append("- Token đo trên model: %s. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token "
               "thật có thể lệch; ghi rõ \"đo trên model X, tính giá model Y\" trong cost/cost-estimate.md." % (", ".join(measured) or "—"))
    out.append("- Phiên lỗi (không tính vào trung bình): %d/%d." % (len(rows) - len(ok), len(rows)))
    if cfg["fx_rate"]:
        out.append("- Tỷ giá: 1 USD = %s ₫ (%s)." % (format(cfg["fx_rate"], ",").replace(",", "."), cfg["fx_source"] or "chưa ghi nguồn"))
    return out


SIM_COLS = ["run_id", "session", "persona", "turns", "inputs", "model", "model_calls", "tool_calls",
            "tokens_in", "tokens_out", "latency_s", "error", "tokens_by_model"]


def pick_rate(models, rate_from=None):
    """Chọn lượt eval đã chấm để lấy tỉ lệ đạt. → (graded | None, other | None).
    rate_from: đường dẫn một lượt cụ thể (vd eval/run-2.csv). Không có thì lấy lượt run-N mới nhất đã chấm xong,
    chạy bằng đúng các model đang đo. graded["why"] giải thích đã chọn lượt nào và vì sao."""
    if rate_from:
        path = rate_from if os.path.isabs(rate_from) else os.path.join(ROOT, rate_from)
        res = ev.grade(path)
        if isinstance(res, str):
            sys.exit("--rate-from %s chưa dùng được:\n%s" % (rate_from, res))
        res["why"] = "Tỉ lệ đạt lấy từ lượt nhóm chọn: %s (--rate-from)." % ev.rel(path)
        if res["models"] != sorted(set(models)):
            res["why"] += " ⚠️ Lượt này chạy bằng %s, mô phỏng đo trên %s — khác model." % (
                ", ".join(res["models"]) or "?", ", ".join(models) or "?")
        return res, None
    graded = ev.latest_graded_run(models)
    if graded:
        eval_dir = os.path.join(ROOT, "eval")
        n_used = int(re.search(r"run-(\d+)", graded["name"]).group(1))
        newer = sorted(int(m.group(1)) for f in os.listdir(eval_dir)
                       for m in [re.fullmatch(r"run-(\d+)\.csv", f)] if m and int(m.group(1)) > n_used)
        graded["why"] = ("Tự chọn: lượt run-N mới nhất đã chấm xong, chạy bằng đúng model đang đo (%s). "
                         "Muốn dùng lượt khác (vd lượt 2): thêm `--rate-from eval/run-2.csv`." % graded["name"])
        if newer:
            graded["why"] += " Lượt mới hơn nhưng chưa chấm xong hoặc khác model, nên KHÔNG dùng: %s." % ", ".join(
                "run-%d" % n for n in newer)
        return graded, None
    return None, ev.latest_graded_run()


def run(try_n=None, wait=0.0, rate_from=None):
    cfg, warn = load_config()
    for w in warn:
        print("⚠️ " + w)
    if rate_from:  # kiểm trước khi gọi model, để không tốn lượt gọi rồi mới báo lỗi
        res = ev.grade(rate_from if os.path.isabs(rate_from) else os.path.join(ROOT, rate_from))
        if isinstance(res, str):
            sys.exit("--rate-from %s chưa dùng được:\n%s" % (rate_from, res))
    bench = ev.load_items()
    n_sessions = try_n or cfg["sessions"]
    if not try_n and n_sessions < 50:
        print("⚠️ sessions = %d — bản nộp cần ≥50 phiên (guide 4.2)." % n_sessions)
    answer, tracing = ev.load_answer()
    plan = plan_sessions(cfg, bench, n_sessions)
    n = ev.next_numbered(COST_DIR, "simulate", ".csv")
    name = "simulate-try" if try_n else "simulate-%d" % n
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = "%s@%s" % (name, stamp)  # đổi theo tên file thật khi lưu (save)
    print("Mô phỏng %d phiên (seed %s)%s ..." % (n_sessions, cfg["seed"], " — CHẠY THỬ" if try_n else ""))
    rows, cases, stopped, first = [], [], False, True
    for sid, persona, inputs in plan:
        agg = {"model_calls": 0, "tool_calls": 0, "tokens_in": 0, "tokens_out": 0, "latency_s": 0.0}
        models, errors, by_model = set(), [], {}
        for t, text in enumerate(inputs, start=1):
            if not first and wait > 0:
                try:
                    time.sleep(wait)
                except KeyboardInterrupt:
                    stopped = True
                    break
            first = False
            try:
                row, events = ev.call_case(answer, tracing, "%s-T%d" % (sid, t), text)
            except NotImplementedError as e:
                sys.exit("Bản chạy thử chưa nối model: %s\nChưa ghi file nào. Xem %s." % (e, ev.DOC))
            except KeyboardInterrupt:
                stopped = True
                break
            cases.append(("%s-T%d" % (sid, t), events))
            for k in agg:
                agg[k] += row[k]
            models.update(m for m in row["model"].split(", ") if m)
            for e in events:  # token theo từng model (bản chạy thử gọi nhiều model thì mỗi model một giá)
                if e.get("kind") == "model" and not e.get("error"):
                    t_m = by_model.setdefault(e.get("model") or "?", {"in": 0, "out": 0})
                    t_m["in"] += e.get("tokens_in") or 0
                    t_m["out"] += e.get("tokens_out") or 0
            if row["error"]:
                errors.append("T%d %s" % (t, row["error"]))
        if stopped:
            break
        rows.append(dict(agg, run_id=run_id, session=sid, persona=persona["name"], turns=len(inputs),
                         inputs=" ‖ ".join(x[:80] for x in inputs), model=", ".join(sorted(models)),
                         latency_s=round(agg["latency_s"], 3), error="; ".join(errors),
                         by_model=by_model, tokens_by_model=json.dumps(by_model, ensure_ascii=False, sort_keys=True)))
        print("  [%d/%d] %s %-12s token vào %d · ra %d%s" % (len(rows), n_sessions, sid, persona["name"],
              agg["tokens_in"], agg["tokens_out"], " · lỗi" if errors else ""))
    if not rows:
        sys.exit("Đã dừng trước khi xong phiên nào. Không ghi file.")

    def save(fname):
        rid = "%s@%s" % (fname, stamp)
        for r in rows:
            r["run_id"] = rid
        path = os.path.join(COST_DIR, fname + ".csv")
        ev.write_csv(path, SIM_COLS, rows)
        ev.write_trace(fname, rid, cases)
        return path

    if stopped:
        path = save("simulate-stopped")
        print("⚠️ Đã dừng giữa chừng (Ctrl+C): %d/%d phiên → %s. KHÔNG tính là một lượt mô phỏng." % (len(rows), n_sessions, ev.rel(path)))
        return 1
    if all(r["error"] for r in rows):
        path = save("simulate-error")
        print("⚠️ Mọi phiên đều lỗi → %s. Lỗi phiên đầu: %s" % (ev.rel(path), rows[0]["error"]))
        return 1
    if ev.looks_mock(rows):
        path = save("simulate-mock")
        print("⚠️ Bản chạy thử chưa gọi model thật (model fake / không gọi model / token = 0) → %s." % ev.rel(path))
        print("   Lượt này KHÔNG được tính. Nối model thật theo %s rồi chạy lại." % ev.DOC)
        return 1
    path = save(name)
    graded, other = pick_rate(measured_models(rows), rate_from)
    lines = summarize(cfg, rows, graded, other)
    md_path = os.path.join(COST_DIR, name + "-summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Tóm tắt mô phỏng %s\n\n" % rows[0]["run_id"])
        f.write("Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.\n\n")
        f.write("\n".join(lines) + "\n")
    print()
    print("\n".join(lines))
    print()
    print("Đã ghi %s · %s · traces/%s.jsonl" % (ev.rel(path), ev.rel(md_path), name))
    if try_n:
        print("ĐÂY LÀ LƯỢT CHẠY THỬ — bản nộp: python run.py simulate (≥50 phiên).")
    return 0


def main(args):
    if any(a in ("-h", "--help", "help") for a in args):
        print(USAGE)
        return 0
    try_n, wait, rate_from, i = None, 0.0, None, 0
    while i < len(args):
        a = args[i]
        if a == "--try":
            try_n = TRY_DEFAULT
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                try:
                    try_n = int(args[i + 1])
                except ValueError:
                    print("Sau --try là số phiên (vd --try 10).\n" + USAGE)
                    return 2
                i += 1
            if try_n < 1:
                print("--try cần số phiên ≥1.")
                return 2
        elif a == "--wait":
            try:
                wait = float(args[i + 1])
                if wait < 0:
                    raise ValueError
            except (IndexError, ValueError):
                print("Sau --wait cần một số giây.\n" + USAGE)
                return 2
            i += 1
        elif a == "--rate-from":
            if i + 1 >= len(args) or args[i + 1].startswith("-"):
                print("Sau --rate-from cần một file lượt đã chấm, vd eval/run-2.csv.\n" + USAGE)
                return 2
            rate_from = args[i + 1]
            i += 1
        else:
            print("Không hiểu tham số: %s\n%s" % (a, USAGE))
            return 2
        i += 1
    return run(try_n=try_n, wait=wait, rate_from=rate_from)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
