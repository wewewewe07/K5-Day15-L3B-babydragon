"""Khung ghi trace — NHÓM KHÔNG CẦN SỬA FILE NÀY.

Mỗi lần gọi model (hàm có @model_call trong ai.py) hoặc gọi công cụ (hàm có @tool trong tools.py),
khung ghi một sự kiện: gọi gì, token vào / ra, mất bao lâu, lỗi gì. Nhờ đó:
  - `python run.py eval` biết mỗi câu thử gọi model mấy lần, hết bao nhiêu token → cột trong eval/run-N.csv
  - `python run.py simulate` tính được chi phí mỗi phiên từ token đo thật
  - trace từng câu được lưu ở traces/run-N.jsonl (mỗi dòng một sự kiện) — giám khảo có thể mở trace
    của một câu trượt để xem AI đã làm gì.

Nhóm chỉ cần:
  - đặt @model_call lên hàm gọi model, hàm đó trả dict có "text", "model", "tokens_in", "tokens_out"
  - đặt @tool lên mỗi công cụ
  - (tuỳ chọn) gọi note("...") để ghi một quyết định hay lý do dừng vào trace.

Chỉ dùng thư viện chuẩn.
"""
import functools
import time

PREVIEW = 300  # số ký tự tối đa của mỗi đoạn xem trước trong trace

TOOLS = {}     # tên công cụ → hàm (điền tự động bởi @tool)

_case = {"id": None, "events": None, "t0": 0.0}


def _short(value):
    text = value if isinstance(value, str) else repr(value)
    return text if len(text) <= PREVIEW else text[:PREVIEW] + "…"


def _record(event):
    if _case["events"] is None:  # đang chạy ngoài khung (vd gọi thẳng hàm) — không ghi
        return
    event["t"] = round(time.perf_counter() - _case["t0"], 3)
    _case["events"].append(event)


def begin(case_id):
    """Khung gọi trước mỗi câu thử / mỗi lượt hỏi."""
    _case.update(id=case_id, events=[], t0=time.perf_counter())


def end():
    """Khung gọi sau mỗi câu thử / lượt hỏi. Trả (tóm tắt, danh sách sự kiện)."""
    events = _case["events"] or []
    _case.update(id=None, events=None)
    models = [e for e in events if e["kind"] == "model"]
    summary = {
        "model_calls": len(models),
        "tool_calls": sum(1 for e in events if e["kind"] == "tool"),
        "tokens_in": sum(e.get("tokens_in") or 0 for e in models),
        "tokens_out": sum(e.get("tokens_out") or 0 for e in models),
        "models": sorted({e.get("model") or "" for e in models} - {""}),
        "errors": [e.get("error") for e in events if e.get("error")],
    }
    return summary, events


def note(text):
    """Ghi một dòng tự do vào trace, vd note("dừng: đủ căn cứ sau 2 bước")."""
    _record({"kind": "note", "text": _short(text)})


def model_call(fn):
    """Đặt lên hàm gọi model. Hàm phải trả dict có text, model, tokens_in, tokens_out."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            res = fn(*args, **kwargs)
        except Exception as e:
            _record({"kind": "model", "name": fn.__name__, "error": "%s: %s" % (type(e).__name__, e),
                     "latency_s": round(time.perf_counter() - t0, 3)})
            raise
        problems = []
        if not isinstance(res, dict):
            problems.append("%s() phải trả dict, đang trả %s" % (fn.__name__, type(res).__name__))
            res_d = {}
        else:
            res_d = res
            for k in ("text", "model", "tokens_in", "tokens_out"):
                if k not in res_d:
                    problems.append("thiếu khoá %s" % k)
            for k in ("tokens_in", "tokens_out"):
                v = res_d.get(k)
                if k in res_d and not (isinstance(v, int) and not isinstance(v, bool) and v >= 0):
                    problems.append("%s phải là số nguyên ≥0, đang là %r" % (k, v))
        event = {
            "kind": "model", "name": fn.__name__,
            "model": str(res_d.get("model") or ""),
            "tokens_in": res_d.get("tokens_in") if isinstance(res_d.get("tokens_in"), int) else 0,
            "tokens_out": res_d.get("tokens_out") if isinstance(res_d.get("tokens_out"), int) else 0,
            "latency_s": round(time.perf_counter() - t0, 3),
            "input": _short(args if not kwargs else (args, kwargs)),
            "output": _short(res_d.get("text", "")),
        }
        if problems:
            event["error"] = "; ".join(problems)
        _record(event)
        if problems:
            raise TypeError("Hợp đồng %s(): %s — xem đầu file codebase/ai.py" % (fn.__name__, "; ".join(problems)))
        return res
    return wrapper


def tool(fn):
    """Đặt lên mỗi công cụ. Khung ghi tên, input, output (rút gọn), thời gian, lỗi."""
    TOOLS[fn.__name__] = fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        event = {"kind": "tool", "name": fn.__name__, "input": _short(args if not kwargs else (args, kwargs))}
        try:
            res = fn(*args, **kwargs)
        except Exception as e:
            event.update(error="%s: %s" % (type(e).__name__, e), latency_s=round(time.perf_counter() - t0, 3))
            _record(event)
            raise
        event.update(output=_short(res), latency_s=round(time.perf_counter() - t0, 3))
        _record(event)
        return res

    TOOLS[fn.__name__] = wrapper
    return wrapper
