"""Bộ chạy đánh giá — KHUNG, nhóm không cần sửa. Thường gọi qua run.py:

  python run.py check                   kiểm eval/benchmark.csv + eval/metric_spec.yaml (chỉ cảnh báo, không sửa file)
  python run.py eval --fake             chạy thử bộ chạy, KHÔNG gọi agent → eval/run-fake.csv
  python run.py eval --try [N]          gọi bản chạy thử cho N câu đầu (mặc định 3) → eval/run-try.csv
  python run.py eval                    chạy cả bộ qua codebase/agent.py → eval/run-N.csv + traces/run-N.jsonl
  python run.py eval --wait 4           như trên, nghỉ 4 giây giữa hai câu (gói miễn phí hay giới hạn lượt / phút)
  python run.py score eval/run-1.csv    tính % đạt sau khi điền cột pass

Cột `pass` để trống: nhóm tự chấm theo pass_criterion và eval/metric_spec.yaml (code, LLM chấm có kiểm tay,
hoặc người chấm) rồi điền 1 / 0. Bộ chạy KHÔNG tự chấm, vì cách chấm là quyết định của nhóm.

Lượt KHÔNG được đánh số run-N (không dùng để báo cáo):
  run-fake.csv (không gọi agent) · run-try.csv (thử vài câu) · run-mock.csv (model giả / token = 0)
  run-error.csv (mọi câu đều lỗi) · run-stopped.csv (bấm Ctrl+C giữa chừng)

Chỉ dùng thư viện chuẩn, Python 3.10 trở lên (3.8–3.9 vẫn chạy).
"""
import csv
import datetime
import io
import json
import os
import re
import sys
import time
import unicodedata

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEBASE = os.path.join(ROOT, "codebase")
BENCH = os.path.join(ROOT, "eval", "benchmark.csv")
METRIC_SPEC = os.path.join(ROOT, "eval", "metric_spec.yaml")
TRACES = os.path.join(ROOT, "traces")
REQUIRED = ["id", "input", "expected", "pass_criterion", "type", "source"]
TYPES = ["thuong", "kho", "tu_choi"]
SOURCE_CODES = ["nguoi_dung", "data_that", "tu_viet", "sinh_seed"]
REAL_SOURCES = {"nguoi_dung", "data_that"}
OUT_COLS = ["run_id", "id", "type", "input", "expected", "pass_criterion", "output", "pass", "ghi_chu",
            "model", "model_calls", "tool_calls", "tokens_in", "tokens_out", "latency_s", "error"]
PASS_YES = {"1", "x", "dat", "đạt"}
PASS_NO = {"0", "khong", "không"}
MOCK_MODELS = {"mock", "fake", ""}
TRY_DEFAULT = 3
NOT_A_RUN = {"run-fake.csv", "run-try.csv", "run-mock.csv", "run-error.csv", "run-stopped.csv"}
DOC = "docs/connect-model.md"

USAGE = """Cách dùng (thường gọi qua run.py):
  python run.py check                   kiểm eval/benchmark.csv + eval/metric_spec.yaml
  python run.py eval --fake             chạy thử bộ chạy, KHÔNG gọi agent → eval/run-fake.csv
  python run.py eval --try [N]          gọi bản chạy thử cho N câu đầu (mặc định 3) → eval/run-try.csv
  python run.py eval                    chạy cả bộ → eval/run-N.csv + traces/run-N.jsonl
  python run.py eval --wait 4           như trên, nghỉ 4 giây giữa hai câu
  python run.py score eval/run-1.csv    tính % đạt sau khi điền cột pass"""


def rel(path):
    """Đường dẫn tính từ thư mục repo, luôn dùng dấu / (Windows cũng vậy)."""
    p = os.path.abspath(path)
    if p == ROOT or p.startswith(ROOT + os.sep):
        p = os.path.relpath(p, ROOT)
    return p.replace(os.sep, "/")


# ================================================================ đọc CSV

def _blank_line(line):
    return not line.strip().strip(",;").strip()


def read_text(path):
    """Đọc file UTF-8 (có hoặc không có BOM), bỏ các dòng trắng ở đầu file."""
    try:
        with open(path, encoding="utf-8-sig", newline="") as f:
            text = f.read()
    except UnicodeDecodeError:
        sys.exit("File %s không phải UTF-8. Trong Excel: File → Save As → chọn \"CSV UTF-8 (Comma delimited)\".\n"
                 "Google Sheets: Tệp → Tải xuống → CSV." % rel(path))
    lines = text.splitlines(True)
    while lines and _blank_line(lines[0]):
        lines.pop(0)
    return "".join(lines)


def detect_delim(text):
    first_line = text.split("\n", 1)[0]
    return ";" if first_line.count(";") > first_line.count(",") else ","


def read_csv(path):
    """→ (tên cột, các dòng không trống, dấu phân cách). UTF-8 có/không BOM; dấu phẩy hoặc chấm phẩy."""
    if not os.path.exists(path):
        d = os.path.dirname(path)
        have = ", ".join(sorted(os.listdir(d))) if os.path.isdir(d) else "(không có thư mục)"
        sys.exit("Không tìm thấy file: %s\nCác file đang có trong %s/: %s" % (rel(path), rel(d), have))
    text = read_text(path)
    delim = detect_delim(text)
    reader = csv.DictReader(io.StringIO(text), delimiter=delim)
    fields = [(c or "").strip() for c in (reader.fieldnames or [])]
    reader.fieldnames = fields
    rows = []
    for r in reader:
        clean = {}
        for k, v in r.items():
            if k is None:  # ô thừa ở cuối dòng (thường do dấu phẩy trong ô chưa đặt trong ngoặc kép)
                clean["__extra__"] = v
                continue
            clean[k] = v if isinstance(v, str) else ""
        if all(not str(v).strip() for k, v in clean.items() if k != "__extra__") and not clean.get("__extra__"):
            continue
        rows.append(clean)
    return fields, rows, delim


def load_items():
    fields, rows, _ = read_csv(BENCH)
    missing = [c for c in REQUIRED if c not in fields]
    if missing:
        sys.exit("eval/benchmark.csv thiếu cột: %s\nDòng đầu phải đúng là: %s" % (", ".join(missing), ",".join(REQUIRED)))
    if not rows:
        sys.exit("eval/benchmark.csv chưa có câu thử nào (chỉ có dòng tiêu đề).")
    return rows


def sample_ids(rows):
    """id các dòng còn chữ "(ví dụ)" (dòng mẫu của khung)."""
    return [r.get("id", "?") for r in rows if "(ví dụ" in " ".join(str(v) for v in r.values())]


def source_code(value):
    """Mã nguồn ở đầu ô source: "nguoi_dung: P2" → "nguoi_dung"."""
    m = re.match(r"\s*([A-Za-z_]+)", value or "")
    return m.group(1).lower() if m else ""


# ================================================================ YAML tối giản (đủ cho metric_spec.yaml, personas.yaml)

class YamlError(ValueError):
    pass


def _strip_comment(s):
    out, quote = [], None
    for i, ch in enumerate(s):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or s[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _split_flow(s):
    parts, cur, quote = [], "", None
    for ch in s:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == ",":
            parts.append(cur)
            cur = ""
            continue
        cur += ch
    parts.append(cur)
    return parts


def _scalar(s, lineno):
    s = s.strip()
    if s in ("", "~", "null"):
        return None
    if s[0] in "\"'":
        if len(s) < 2 or s[-1] != s[0]:
            raise YamlError("dòng %d: thiếu dấu %s đóng chuỗi" % (lineno, s[0]))
        return s[1:-1]
    if s.startswith("["):
        if not s.endswith("]"):
            raise YamlError("dòng %d: danh sách [ ... ] thiếu dấu ]" % lineno)
        inner = s[1:-1].strip()
        return [_scalar(x, lineno) for x in _split_flow(inner)] if inner else []
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    for cast in (int, float):
        try:
            return cast(s)
        except ValueError:
            pass
    return s


_KEY = re.compile(r"^([^\s\"'\[\]{}#\-][^:]*?|\"[^\"]*\"|'[^']*'):(?:\s+(.*))?$")


def _parse_block(lines, i, indent):
    if lines[i][2] == "-" or lines[i][2].startswith("- "):
        return _parse_list(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_list(lines, i, indent):
    out = []
    while i < len(lines):
        lineno, cur, text = lines[i]
        if cur < indent or not (text == "-" or text.startswith("- ")):
            break
        if cur > indent:
            raise YamlError("dòng %d: thụt lề không khớp" % lineno)
        rest = text[1:].lstrip()
        if not rest:
            if i + 1 < len(lines) and lines[i + 1][1] > indent:
                val, i = _parse_block(lines, i + 1, lines[i + 1][1])
            else:
                val, i = None, i + 1
            out.append(val)
        elif _KEY.match(rest):
            col = cur + len(text) - len(rest)
            lines[i] = (lineno, col, rest)
            val, i = _parse_map(lines, i, col)
            out.append(val)
        else:
            out.append(_scalar(rest, lineno))
            i += 1
    return out, i


def _parse_map(lines, i, indent):
    out = {}
    while i < len(lines):
        lineno, cur, text = lines[i]
        if cur < indent or (text == "-" or text.startswith("- ")):
            break
        if cur > indent:
            raise YamlError("dòng %d: thụt lề không khớp (thừa hoặc thiếu dấu cách?)" % lineno)
        m = _KEY.match(text)
        if not m:
            raise YamlError("dòng %d: cần dạng \"tên: giá trị\", đang là: %s" % (lineno, text))
        key = m.group(1).strip().strip("\"'")
        rest = (m.group(2) or "").strip()
        if key in out:
            raise YamlError("dòng %d: tên \"%s\" bị lặp" % (lineno, key))
        i += 1
        if rest:
            out[key] = _scalar(rest, lineno)
        elif i < len(lines) and (lines[i][1] > indent or (lines[i][1] == indent and lines[i][2].startswith("-"))):
            out[key], i = _parse_block(lines, i, lines[i][1])
        else:
            out[key] = None
    return out, i


def load_yaml(path):
    """Đọc một tập con đơn giản của YAML: tên: giá trị, danh sách "- ", chuỗi trong ngoặc kép, [a, b], # chú thích."""
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read().splitlines()
    lines = []
    for n, line in enumerate(raw, start=1):
        if "\t" in line[:len(line) - len(line.lstrip())]:
            raise YamlError("dòng %d: dùng dấu cách để thụt lề, không dùng Tab" % n)
        body = _strip_comment(line)
        if body.strip():
            lines.append((n, len(body) - len(body.lstrip()), body.strip()))
    if not lines:
        return {}
    value, i = _parse_block(lines, 0, lines[0][1])
    if i < len(lines):
        raise YamlError("dòng %d: thụt lề không khớp với các dòng phía trên" % lines[i][0])
    return value


def placeholder(v):
    return v is None or (isinstance(v, str) and (not v.strip() or v.strip().startswith("<")))


# ================================================================ check

def check_metric_spec():
    warn = []
    if not os.path.exists(METRIC_SPEC):
        return ["Chưa có eval/metric_spec.yaml (guide bước 2.4)."]
    try:
        spec = load_yaml(METRIC_SPEC)
    except YamlError as e:
        return ["eval/metric_spec.yaml đọc không được: %s" % e]
    metrics = spec.get("metrics") if isinstance(spec, dict) else None
    if not isinstance(metrics, list):
        return ["eval/metric_spec.yaml cần mục \"metrics:\" là danh sách (- name: …)."]
    done = 0
    for k, m in enumerate(metrics, start=1):
        if not isinstance(m, dict):
            warn.append("metric thứ %d không đúng dạng (cần name, definition, grader, threshold)." % k)
            continue
        empty = [f for f in ("name", "definition", "grader", "threshold") if placeholder(m.get(f))]
        if empty:
            warn.append("metric %s còn trống / còn mẫu <…> ở: %s." % (m.get("name") or "#%d" % k, ", ".join(empty)))
        else:
            done += 1
    print("  eval/metric_spec.yaml: %d metric đã điền đủ (cần ≥3)" % done)
    if done < 3:
        warn.append("Cần ≥3 metric điền đủ name · definition · grader · threshold (đang có %d)." % done)
    return warn


TEAMS = os.path.join(ROOT, "TEAMS.md")
TEAMS_HEADER = ["STT", "Họ và tên", "Mã học viên", "Vai trò", "Phần việc chính"]
TEAMS_FIELDS = ["Tên nhóm", "Lớp", "Track", "Link repo"]


def check_teams():
    """Kiểm TEAMS.md đúng format để BTC quét ghép điểm. → danh sách cảnh báo."""
    print("Kiểm TEAMS.md")
    if not os.path.exists(TEAMS):
        return ["Chưa có TEAMS.md ở thư mục gốc repo (chép từ starter-repo, điền đúng mẫu)."]
    # NFC: chữ có dấu chép từ một số trình soạn / macOS có thể ở dạng tổ hợp (NFD), nhìn giống hệt nhưng so chuỗi sai
    text = unicodedata.normalize("NFC", read_text(TEAMS))
    warn = []
    fields = {}
    for line in text.splitlines():
        m = re.match(r"\s*-\s*([^:]+?)\s*:\s*(.*)$", line)
        if m and m.group(1).strip() in TEAMS_FIELDS:
            fields[m.group(1).strip()] = m.group(2).strip()
    for f in TEAMS_FIELDS:
        v = fields.get(f)
        if v is None:
            warn.append("TEAMS.md thiếu dòng \"- %s: …\" (giữ nguyên các dòng của mẫu)." % f)
        elif not v or "____" in v:
            warn.append("TEAMS.md: dòng \"%s\" chưa điền." % f)
    if fields.get("Lớp") and "____" not in fields["Lớp"] and fields["Lớp"] not in ("L3A", "L3B"):
        warn.append("TEAMS.md: Lớp ghi đúng L3A hoặc L3B (đang ghi %r)." % fields["Lớp"])
    if fields.get("Track") and "____" not in fields["Track"] and fields["Track"] not in ("A", "B", "C", "D", "E", "F"):
        warn.append("TEAMS.md: Track ghi một chữ A, B, C, D, E hoặc F (đang ghi %r)." % fields["Track"])
    # Gom các bảng markdown; dùng bảng có tiêu đề đúng mẫu (nhóm có thể thêm bảng khác trên / dưới).
    tables, cur = [], None
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            cur = None
            continue
        # tách ô theo "|" nhưng giữ "\|" (dấu | trong nội dung ô)
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if cur is None:
            cur = {"header": cells, "rows": []}
            tables.append(cur)
        elif not all(set(c) <= set("-: ") for c in cells):
            cur["rows"].append(cells)
    table = next((t for t in tables if t["header"] == TEAMS_HEADER), tables[0] if tables else None)
    header, rows = (table["header"], table["rows"]) if table else (None, [])
    if header != TEAMS_HEADER:
        warn.append("TEAMS.md: tiêu đề bảng phải đúng là | %s | (đang là | %s |)."
                    % (" | ".join(TEAMS_HEADER), " | ".join(header or [])))
        return warn
    print("  %d thành viên" % len(rows))
    if not 3 <= len(rows) <= 5:
        warn.append("TEAMS.md: nhóm 3–5 người, bảng đang có %d dòng." % len(rows))
    ids, leaders = [], 0
    for k, r in enumerate(rows, start=1):
        if len(r) != len(TEAMS_HEADER):
            warn.append("TEAMS.md dòng %d: cần đúng %d cột." % (k, len(TEAMS_HEADER)))
            continue
        _, name, sid, role, _ = r
        if not name or "____" in name:
            warn.append("TEAMS.md dòng %d: chưa điền Họ và tên." % k)
        if not sid or "____" in sid:
            warn.append("TEAMS.md dòng %d: chưa điền Mã học viên." % k)
        elif re.search(r"\s", sid):
            warn.append("TEAMS.md dòng %d: Mã học viên không được có khoảng trắng." % k)
        else:
            ids.append(sid)
        if role not in ("Đội trưởng", "Thành viên"):
            warn.append("TEAMS.md dòng %d: Vai trò ghi đúng chữ \"Đội trưởng\" hoặc \"Thành viên\"." % k)
        if role == "Đội trưởng":
            leaders += 1
            if k != 1:
                warn.append("TEAMS.md: Đội trưởng phải ở dòng 1.")
    if leaders != 1:
        warn.append("TEAMS.md: cần đúng 1 Đội trưởng (đang có %d)." % leaders)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        warn.append("TEAMS.md: Mã học viên bị trùng: %s." % ", ".join(dup))
    return warn


def check():
    fields, rows, delim = read_csv(BENCH)
    print("Kiểm eval/benchmark.csv")
    if delim == ";":
        print("  (file dùng dấu chấm phẩy — vẫn đọc được; bộ chạy ghi kết quả bằng dấu phẩy)")
    missing = [c for c in REQUIRED if c not in fields]
    print("  ⚠️ Thiếu cột: %s. Dòng đầu phải đúng là: %s" % (", ".join(missing), ",".join(REQUIRED)) if missing
          else "  Đủ 6 cột: %s" % ",".join(REQUIRED))
    n = len(rows)
    counts = {t: 0 for t in TYPES}
    other, src = {}, {c: 0 for c in SOURCE_CODES}
    bad_src = []
    for r in rows:
        t = r.get("type", "").strip()
        if t in counts:
            counts[t] += 1
        else:
            other[t or "(trống)"] = other.get(t or "(trống)", 0) + 1
        c = source_code(r.get("source"))
        if c in src:
            src[c] += 1
        else:
            bad_src.append(r.get("id", "?"))
    real = sum(src[c] for c in REAL_SOURCES)
    print("  Số câu thử: %d  ·  thuong %d  ·  kho %d  ·  tu_choi %d" % (n, counts["thuong"], counts["kho"], counts["tu_choi"]))
    print("  Nguồn: %s  ·  từ người dùng / data thật: %d/%d"
          % ("  ·  ".join("%s %d" % (c, src[c]) for c in SOURCE_CODES), real, n))
    warn = []
    if other:
        warn.append("Cột type có giá trị lạ: %s. Chỉ dùng thuong / kho / tu_choi."
                    % ", ".join("%s (%d)" % kv for kv in other.items()))
    if n < 10:
        warn.append("Mới %d câu — CP2 cần ≥10." % n)
    if n < 20 or n > 30:
        warn.append("CP3 cần 20–30 câu (đang có %d)." % n)
    if counts["kho"] < 5:
        warn.append("Cần ≥5 câu kho (đang có %d)." % counts["kho"])
    if counts["tu_choi"] < 2:
        warn.append("Cần ≥2 câu tu_choi, gồm 2 câu tấn công (đang có %d)." % counts["tu_choi"])
    if bad_src:
        warn.append("Cột source phải bắt đầu bằng một trong: %s (có thể thêm chi tiết sau dấu :, vd \"nguoi_dung: P2\"). "
                    "Đang sai ở: %s." % (", ".join(SOURCE_CODES), ", ".join(bad_src[:15])))
    if n and real * 3 < n:
        warn.append("Cần ≥1/3 câu từ lời người dùng hoặc data thật (nguoi_dung / data_that): đang %d/%d." % (real, n))
    for col in ("id", "input", "expected", "pass_criterion"):
        if col in fields:
            empty = [r.get("id", "").strip() or "(dòng không id)" for r in rows if not r.get(col, "").strip()]
            if empty:
                warn.append("Cột %s còn trống ở: %s." % (col, ", ".join(empty)))
    ids = [r.get("id", "").strip() for r in rows if r.get("id", "").strip()]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        warn.append("id bị trùng: %s." % ", ".join(dup))
    extra = [r.get("id", "?") for r in rows if r.get("__extra__")]
    if extra:
        warn.append("Câu %s có nhiều ô hơn số cột: ô có dấu phẩy phải đặt trong ngoặc kép \"...\"." % ", ".join(extra))
    if sample_ids(rows):
        warn.append("Còn dòng mẫu \"(ví dụ)\": %s — xoá trước khi nộp." % ", ".join(sample_ids(rows)))
    warn += check_metric_spec()
    warn += check_teams()
    if warn:
        print("Cần xem lại:")
        for w in warn:
            print("  ⚠️ " + w)
    else:
        print("Không thấy vấn đề. Nhớ: mỗi pass_criterion phải kiểm được (đọc output là biết đạt hay không).")
    print("(Lệnh này chỉ kiểm, không sửa file.)")
    return 0


# ================================================================ chạy

def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path

def load_answer():
    """Nạp codebase/agent.py và tracing. Lỗi thì in lời nhắn dễ hiểu và thoát."""
    if CODEBASE not in sys.path:
        sys.path.insert(0, CODEBASE)
    try:
        import tracing  # noqa: E402
        import agent  # noqa: E402
    except Exception as e:
        sys.exit("Không nạp được codebase/ — lỗi ở %s: %s: %s\nSửa lỗi rồi chạy lại. Cách nối model: %s"
                 % (_where(e), type(e).__name__, e, DOC))
    if not hasattr(agent, "answer"):
        sys.exit("codebase/agent.py chưa có hàm answer(text). Xem hợp đồng ở đầu file agent.py.")
    return agent.answer, tracing


def call_case(answer, tracing, case_id, text):
    """Chạy một đầu vào qua answer() trong khung trace. → (dòng kết quả, danh sách sự kiện trace)."""
    tracing.begin(case_id)
    t0 = time.perf_counter()
    output, err = "", ""
    try:
        res = answer(text)
        if isinstance(res, dict) and isinstance(res.get("output"), str):
            output = res["output"]
        elif isinstance(res, str):
            output = res
        else:
            err = "answer() phải trả dict có khoá \"output\" là chuỗi; đang trả %r" % (type(res).__name__,)
    except NotImplementedError:
        tracing.end()
        raise
    except KeyboardInterrupt:
        tracing.end()
        raise
    except Exception as e:  # lỗi của một câu: ghi lại, chạy tiếp câu sau
        err = "%s: %s" % (type(e).__name__, e)
    summary, events = tracing.end()
    row = {"output": output, "model": ", ".join(summary["models"]),
           "model_calls": summary["model_calls"], "tool_calls": summary["tool_calls"],
           "tokens_in": summary["tokens_in"], "tokens_out": summary["tokens_out"],
           "latency_s": round(time.perf_counter() - t0, 3), "error": err}
    return row, events


def looks_mock(rows):
    """Mọi câu không lỗi đều không gọi model thật (model fake / không gọi model / token = 0)."""
    ok = [r for r in rows if not r["error"]]
    if not ok:
        return False
    if all(not r["model_calls"] for r in ok):
        return True
    if all({m.strip().lower() for m in r["model"].split(",")} <= MOCK_MODELS for r in ok):
        return True
    return all(r["tokens_in"] == 0 and r["tokens_out"] == 0 for r in ok)


def next_numbered(folder, stem, ext):
    """Số lượt tiếp theo = số lớn nhất đang có + 1. Không lấp chỗ trống: lượt đã xoá vẫn để lại dấu (run-1, run-3…)."""
    pat = re.compile(r"%s-(\d+)%s$" % (re.escape(stem), re.escape(ext)))
    nums = [int(m.group(1)) for f in (os.listdir(folder) if os.path.isdir(folder) else []) for m in [pat.match(f)] if m]
    return max(nums) + 1 if nums else 1


def write_csv(path, cols, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_trace(name, run_id, cases, header=None):
    """cases: [(case_id, events)] → traces/<name>.jsonl, mỗi dòng một sự kiện.
    header: sự kiện đầu file (vd danh sách id của bộ câu thử lúc chạy) — `score` dùng để kiểm lượt đủ bộ."""
    os.makedirs(TRACES, exist_ok=True)
    path = os.path.join(TRACES, name + ".jsonl")
    with open(path, "w", encoding="utf-8") as f:
        if header:
            f.write(json.dumps(dict({"run_id": run_id, "case": ""}, **header), ensure_ascii=False) + "\n")
        for case_id, events in cases:
            for e in events:
                f.write(json.dumps(dict({"run_id": run_id, "case": case_id}, **e), ensure_ascii=False, default=str) + "\n")
    return path


def fake_case(text):
    return {"output": "[FAKE] " + text[:40], "model": "fake", "model_calls": 0, "tool_calls": 0,
            "tokens_in": 0, "tokens_out": 0, "latency_s": 0.0, "error": ""}, []


def run(mode="real", wait=0.0, try_n=TRY_DEFAULT):
    """mode: "fake" (không gọi agent) · "try" (vài câu đầu) · "real" (lượt thật)."""
    items = load_items()
    if mode == "try":
        items = items[:try_n]
    if mode != "fake" and sample_ids(items):
        print("⚠️ eval/benchmark.csv còn dòng mẫu \"(ví dụ)\": %s. Vẫn chạy, nhưng nhớ thay bằng câu thử của nhóm."
              % ", ".join(sample_ids(items)))
    ids = [it.get("id", "").strip() for it in items]
    dup = sorted({i for i in ids if i and ids.count(i) > 1})
    if dup and mode != "fake":
        sys.exit("eval/benchmark.csv có id bị trùng: %s — mỗi câu thử một id. Sửa rồi chạy lại "
                 "(chưa gọi model, chưa ghi file nào). Kiểm: python run.py check" % ", ".join(dup))
    answer = tracing = None
    if mode != "fake":
        answer, tracing = load_answer()
    n = next_numbered(os.path.join(ROOT, "eval"), "run", ".csv")
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = {"fake": "run-fake", "try": "run-try"}.get(mode, "run-%d" % n)
    run_id = "%s@%s" % (name, stamp)  # đổi theo tên file thật khi lưu (save)

    note = {"fake": " (KHÔNG gọi agent)", "try": " — LƯỢT THỬ, không tính là một lượt"}.get(mode, "")
    print("Chạy %d câu%s ..." % (len(items), note))
    rows, cases, stopped = [], [], False
    for idx, it in enumerate(items):
        if idx and wait > 0:
            try:
                time.sleep(wait)
            except KeyboardInterrupt:
                stopped = True
                break
        try:
            if mode == "fake":
                row, events = fake_case(it.get("input", ""))
            else:
                row, events = call_case(answer, tracing, it.get("id", ""), it.get("input", ""))
        except NotImplementedError as e:
            if idx == 0:
                sys.exit("Bản chạy thử chưa nối model: %s\nChưa ghi file nào. Làm theo %s, rồi thử `python run.py eval --try`."
                         % (e, DOC))
            row, events = dict(fake_case("")[0], output="", model=""), []
            row["error"] = "NotImplementedError: %s" % e
        except KeyboardInterrupt:
            stopped = True
            break
        row.update({"run_id": run_id, "id": it.get("id", ""), "type": it.get("type", ""), "input": it.get("input", ""),
                    "expected": it.get("expected", ""), "pass_criterion": it.get("pass_criterion", ""),
                    "pass": "", "ghi_chu": ""})
        if not row["error"] and not row["output"].strip():
            row["ghi_chu"] = "output rỗng"
        rows.append(row)
        if mode != "fake":  # kết quả cuối đưa cho người dùng — để đối chiếu cột output với trace
            events = list(events) + [{"kind": "final", "output": row["output"], "error": row["error"]}]
        cases.append((row["id"], events))
        if mode == "try" and not row["error"]:
            mark = "xong · model %s · gọi model %d · công cụ %d · token vào %s · ra %s" % (
                row["model"] or "—", row["model_calls"], row["tool_calls"], row["tokens_in"], row["tokens_out"])
        else:
            mark = ("lỗi: " + row["error"]) if row["error"] else "xong"
        print("  [%d/%d] %s %s" % (idx + 1, len(items), row["id"], mark))

    if not rows:
        sys.exit("Đã dừng trước khi chạy xong câu nào. Không ghi file.")
    n_err = sum(1 for r in rows if r["error"])
    eval_dir = os.path.join(ROOT, "eval")

    def save(fname):
        rid = "%s@%s" % (fname, stamp)
        for r in rows:
            r["run_id"] = rid
        path = os.path.join(eval_dir, fname + ".csv")
        write_csv(path, OUT_COLS, rows)
        # đầu trace: danh sách id của bộ câu thử LÚC CHẠY → `score` kiểm lượt đủ bộ theo đúng bộ này,
        # nên thêm câu thử về sau (được phép) không làm lượt cũ hết chấm được
        header = {"kind": "bench", "ids": ids} if mode == "real" else None
        trace_path = write_trace(fname, rid, cases, header) if mode != "fake" else None
        return path, trace_path

    if stopped:
        path, _ = save("run-stopped" if mode == "real" else name)
        print("⚠️ Đã dừng giữa chừng (Ctrl+C): mới chạy %d/%d câu → %s. KHÔNG tính là một lượt."
              % (len(rows), len(items), rel(path)))
        return 1
    if mode == "try":
        path, tpath = save("run-try")
        print("Đã ghi %s và %s (ghi đè mỗi lần thử; không tính là một lượt)." % (rel(path), rel(tpath)))
        if n_err == len(rows):
            print("⚠️ Cả %d câu đều lỗi. Xem cột error trong %s và %s mục \"Lỗi hay gặp\"." % (len(rows), rel(path), DOC))
            return 1
        if looks_mock(rows):
            print("⚠️ Bản chạy thử chưa gọi model thật (model fake, không gọi model, hoặc token = 0).")
            print("   Đang ở chế độ giả? Điền MODEL_PROVIDER trong .env và viết phần gọi model trong codebase/ai.py (%s)." % DOC)
            return 1
        print("Nối model được: có token > 0. Bước tiếp: python run.py eval")
        if n_err:
            print("Lưu ý: %d câu lỗi — xem cột error." % n_err)
        return 0
    if mode == "fake":
        path, _ = save("run-fake")
        print("Đã chạy %d câu → %s. ĐÂY LÀ LƯỢT THỬ KHÔNG GỌI AGENT — không dùng để báo cáo." % (len(rows), rel(path)))
        return 0
    if n_err == len(rows):
        path, _ = save("run-error")
        print("⚠️ Cả %d câu đều lỗi → chưa tính là một lượt (ghi %s, không tạo run-N.csv)." % (len(rows), rel(path)))
        print("Lỗi của câu đầu: %s\nSửa codebase/ hoặc .env rồi chạy lại. Xem %s mục \"Lỗi hay gặp\"." % (rows[0]["error"], DOC))
        return 1
    if looks_mock(rows):
        path, _ = save("run-mock")
        print("=" * 70)
        print("⚠️ BẢN CHẠY THỬ CHƯA GỌI MODEL THẬT: mọi câu dùng model fake, không gọi model, hoặc token = 0.")
        print("   Lượt này KHÔNG được tính: ghi %s, KHÔNG tạo run-N.csv." % rel(path))
        print("   Nối model thật theo %s, thử `python run.py eval --try`, rồi chạy lại `python run.py eval`." % DOC)
        print("=" * 70)
        return 1
    path, tpath = save(name)
    print("Đã chạy %d/%d câu → %s · trace %s · lỗi: %d" % (len(rows), len(items), rel(path), rel(tpath), n_err))
    print("Run ID: %s" % rows[0]["run_id"])
    if n_err:
        print("Xem cột error trong %s. Lượt có câu lỗi kỹ thuật: ghi rõ trong eval/report.md, có thể chạy lại thành lượt mới." % rel(path))
    empty = [r["id"] for r in rows if r.get("ghi_chu") == "output rỗng"]
    if empty:
        print("⚠️ %d câu model trả về RỖNG (không báo lỗi): %s — thường do hết số token ra tối đa hoặc bộ lọc an toàn. "
              "Đã ghi \"output rỗng\" ở cột ghi_chu. Xem %s mục \"Lỗi hay gặp\"." % (len(empty), ", ".join(empty[:15]), DOC))
    ok = [r for r in rows if not r["error"]]
    if ok:
        print("Trung bình mỗi câu: gọi model %.1f lần · công cụ %.1f lần · token vào %.0f · ra %.0f"
              % tuple(sum(r[k] for r in ok) / len(ok) for k in ("model_calls", "tool_calls", "tokens_in", "tokens_out")))
    print("Tiếp theo: mở %s, điền cột pass (1/0) theo pass_criterion và eval/metric_spec.yaml, rồi chạy:" % rel(path))
    print("  python run.py score %s" % rel(path))
    return 0


# ================================================================ score

def grade(path):
    """Đọc một file lượt đã chấm. → dict kết quả, hoặc chuỗi lý do chưa dùng được."""
    fields, rows, _ = read_csv(path)
    if "pass" not in fields:
        return "File %s không có cột pass. Dùng file do `python run.py eval` tạo (eval/run-N.csv)." % rel(path)
    if not rows:
        return "File %s chưa có câu nào." % rel(path)
    ids = [r.get("id", "").strip() for r in rows]
    dup = sorted({i for i in ids if i and ids.count(i) > 1})
    if dup:
        return "ID LẶP: %s — mỗi id giữ đúng một dòng." % ", ".join(dup[:15])
    name = os.path.basename(path)
    if name != "run-try.csv":  # run-try chỉ chạy vài câu đầu, cố ý không đủ bộ
        bench, where = bench_at_run_time(path)
        missing = [i for i in bench if i and i not in set(ids)]
        if missing:
            return ("CHƯA ĐỦ BỘ: file thiếu %d câu của %s (%s). Một lượt phải chạy đủ cả bộ."
                    % (len(missing), where, ", ".join(missing[:15])))
    graded, blank, odd = [], [], []
    for r in rows:
        v = unicodedata.normalize("NFC", r.get("pass", "")).strip().lower()
        if v in PASS_YES:
            graded.append((r, 1))
        elif v in PASS_NO:
            graded.append((r, 0))
        elif v:
            odd.append("%s (%r)" % (r.get("id", "?"), r.get("pass")))
        else:
            blank.append(r.get("id", "?") or "?")
    if blank or odd:
        msg = "CHƯA CHẤM XONG: đã chấm %d/%d câu." % (len(graded), len(rows))
        if blank:
            msg += "\n  Cột pass còn trống: %s%s" % (", ".join(blank[:15]), " ..." if len(blank) > 15 else "")
        if odd:
            msg += "\n  Cột pass có giá trị lạ: %s. Dùng 1 (đạt) hoặc 0 (không đạt)." % ", ".join(odd)
        return msg
    by_type = {}
    for r, p in graded:
        t = r.get("type", "")
        a, b = by_type.get(t, (0, 0))
        by_type[t] = (a + p, b + 1)
    # câu lỗi kỹ thuật / output rỗng mà vẫn chấm đạt: không đổi số, nhưng nêu rõ để nhóm và giám khảo thấy
    odd_pass = [r.get("id", "?") for r, p in graded
                if p and (r.get("error", "").strip() or not r.get("output", "").strip())]
    return {"path": path, "name": name, "passed": sum(p for _, p in graded), "total": len(rows),
            "by_type": by_type, "run_id": next((r.get("run_id") for r in rows if r.get("run_id")), ""),
            "model": next((r.get("model") for r in rows if r.get("model")), ""),
            "models": sorted({m for r in rows for m in (r.get("model") or "").split(", ") if m}),
            "errors": sum(1 for r in rows if r.get("error", "").strip()),
            "odd_pass": odd_pass, "trace_mismatch": trace_mismatch(path, rows)}


def trace_mismatch(path, rows):
    """Câu có output / token trong file lượt KHÁC với trace của chính lượt đó (file bị sửa tay sau khi chạy).
    Chỉ kiểm được lượt có sự kiện "final" trong trace (bộ chạy ghi từ bản này trở đi). → danh sách id."""
    stem = os.path.splitext(os.path.basename(path))[0]
    trace = os.path.join(TRACES, stem + ".jsonl")
    if not os.path.exists(trace):
        return []
    final, tok = {}, {}
    with open(trace, encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except ValueError:
                continue
            c = e.get("case")
            if e.get("kind") == "final":
                final[c] = e.get("output") or ""
            elif e.get("kind") == "model" and not e.get("error"):
                t = tok.setdefault(c, [0, 0])
                t[0] += e.get("tokens_in") or 0
                t[1] += e.get("tokens_out") or 0
    if not final:
        return []
    bad = []
    for r in rows:
        i = r.get("id", "").strip()
        if i not in final:
            bad.append(i)
            continue
        norm = lambda s: re.sub(r"\s+", " ", (s or "").replace("\r\n", "\n")).strip()  # noqa: E731 — Excel đổi xuống dòng / khoảng trắng
        same_out = norm(r.get("output")) == norm(final[i])
        try:
            same_tok = [int(r.get("tokens_in") or 0), int(r.get("tokens_out") or 0)] == tok.get(i, [0, 0])
        except ValueError:
            same_tok = False
        if not (same_out and same_tok):
            bad.append(i)
    return bad


def bench_at_run_time(path):
    """Danh sách id của bộ câu thử lúc chạy lượt này. → (ids, mô tả nguồn).
    Lấy từ dòng đầu traces/<tên lượt>.jsonl (bộ chạy ghi từ bản này trở đi); lượt cũ không có thì dùng
    eval/benchmark.csv hiện tại như trước."""
    stem = os.path.splitext(os.path.basename(path))[0]
    trace = os.path.join(TRACES, stem + ".jsonl")
    if os.path.exists(trace):
        try:
            with open(trace, encoding="utf-8") as f:
                first = json.loads(f.readline() or "{}")
            if first.get("kind") == "bench" and isinstance(first.get("ids"), list):
                return [str(i).strip() for i in first["ids"]], "bộ câu thử lúc chạy (traces/%s.jsonl)" % stem
        except ValueError:
            pass
    bench = [r.get("id", "").strip() for r in read_csv(BENCH)[1]] if os.path.exists(BENCH) else []
    return bench, "eval/benchmark.csv"


def score(path):
    if not os.path.isabs(path):
        path = os.path.join(ROOT, path)
    res = grade(path)
    print("Chấm %s" % rel(path))
    if isinstance(res, str):
        print("=" * 70)
        print(res)
        print("=" * 70)
        print("Số hiện tại CHƯA dùng được cho báo cáo.")
        return 1
    print("Run ID: %s · model: %s" % (res["run_id"] or "—", ", ".join(res["models"]) or "—"))
    print("Tổng: %d/%d đạt (%.0f%%)" % (res["passed"], res["total"], 100.0 * res["passed"] / res["total"]))
    print("Theo type (đạt / số câu):")
    for t in TYPES + sorted(set(res["by_type"]) - set(TYPES)):
        if t in res["by_type"]:
            a, b = res["by_type"][t]
            print("  %-8s %d/%d (%.0f%%)" % (t or "(trống)", a, b, 100.0 * a / b))
    if res["errors"]:
        print("Lưu ý: %d câu có lỗi khi chạy (cột error) — nói rõ trong eval/report.md." % res["errors"])
    if res["trace_mismatch"]:
        print("⚠️ %d câu có output / token KHÁC trace của lượt này (traces/%s.jsonl): %s — file lượt đã bị sửa sau khi chạy? "
              "Chỉ điền cột pass và ghi_chu, không sửa cột khác." % (len(res["trace_mismatch"]),
              os.path.splitext(res["name"])[0], ", ".join(res["trace_mismatch"][:15])))
    if res["odd_pass"]:
        print("⚠️ %d câu chấm ĐẠT nhưng có lỗi khi chạy hoặc output rỗng: %s — xem lại cách chấm các câu này."
              % (len(res["odd_pass"]), ", ".join(res["odd_pass"][:15])))
    if res["name"] in NOT_A_RUN:
        print("File này KHÔNG phải một lượt đánh giá — không chép vào báo cáo.")
    else:
        print("Chép các số này vào eval/report.md và bảng các lượt chạy trong eval/README.md.")
    return 0


def latest_graded_run(models=None):
    """Lượt run-N.csv mới nhất đã chấm xong. → dict của grade(), hoặc None.
    models: danh sách model — chỉ nhận lượt chạy bằng đúng các model đó (để tỉ lệ đạt khớp model đang đo)."""
    eval_dir = os.path.join(ROOT, "eval")
    runs = sorted((int(m.group(1)), f) for f in os.listdir(eval_dir) for m in [re.fullmatch(r"run-(\d+)\.csv", f)] if m)
    want = sorted(set(models)) if models else None
    for _, f in reversed(runs):
        res = grade(os.path.join(eval_dir, f))
        if isinstance(res, dict) and (want is None or res["models"] == want):
            return res
    return None


# ================================================================ main

def usage_error(msg):
    print(msg, file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 2


def main(args):
    """Kiểm hết tham số TRƯỚC khi nạp codebase/."""
    if any(a in ("-h", "--help", "help") for a in args):
        print(USAGE)
        return 0
    if args[:1] == ["--check"]:
        return check() if len(args) == 1 else usage_error("check không nhận thêm tham số.")
    if args[:1] == ["--score"]:
        if len(args) != 2:
            return usage_error("score cần đúng một file. Ví dụ: python run.py score eval/run-1.csv")
        return score(args[1])
    mode, wait, try_n, i = "real", 0.0, TRY_DEFAULT, 0
    while i < len(args):
        a = args[i]
        if a == "--fake":
            if "--try" in args:
                return usage_error("Không dùng --fake cùng --try.")
            mode = "fake"
        elif a == "--try":
            mode = "try"
            if i + 1 < len(args) and not args[i + 1].startswith("-"):
                try:
                    try_n = int(args[i + 1])
                except ValueError:
                    return usage_error("Sau --try là số câu muốn thử (vd --try 5), không phải %r." % args[i + 1])
                if try_n < 1:
                    return usage_error("--try cần số câu ≥1.")
                i += 1
        elif a == "--wait":
            try:
                wait = float(args[i + 1])
                if wait < 0:
                    raise ValueError
            except (IndexError, ValueError):
                return usage_error("Sau --wait cần một số giây, ví dụ: python run.py eval --wait 4")
            i += 1
        else:
            return usage_error("Không hiểu tham số: %s" % a)
        i += 1
    return run(mode=mode, wait=wait, try_n=try_n)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
