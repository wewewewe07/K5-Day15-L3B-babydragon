"""Giao diện web cho bot kiểm duyệt kịch bản bài giảng (Track A3). Chỉ dùng thư viện chuẩn Python.

Chạy:   python ui/server.py            → mở http://127.0.0.1:8765
        python ui/server.py --port 9000
Gọi đúng hàm answer() của codebase/agent.py (cùng luồng với `python run.py` và `run.py eval`).
"""
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "codebase"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import tracing  # noqa: E402
from agent import answer  # noqa: E402
from tools import split_claims  # noqa: E402
import re  # noqa: E402
import ai  # noqa: E402

LOCK = threading.Lock()  # tracing dùng trạng thái chung → xử lý tuần tự từng yêu cầu
HERE = os.path.dirname(os.path.abspath(__file__))


def load_sources():
    with open(os.path.join(ROOT, "data", "course_sources.json"), encoding="utf-8-sig") as f:
        return json.load(f)


CODE_RE = re.compile(r"SRC-D\d{2}-M\d-\d{2}")


def build_pipeline(text, events, output):
    """Dựng lại 5 bước của workflow (spec §4) từ trace của lượt vừa chạy — chỉ để hiển thị, không ảnh hưởng kết quả."""
    tools = [e for e in events if e.get("kind") == "tool"]
    model = [e for e in events if e.get("kind") == "model"]
    notes = [e.get("text", "") for e in events if e.get("kind") == "note"]
    searched = [e for e in tools if e.get("name") == "search_sources"]
    segs = [e for e in tools if e.get("name") == "get_segment"]
    read = []
    for e in segs:
        for c in CODE_RE.findall(str(e.get("output", ""))):
            if c not in read:
                read.append(c)
    chk = next((e for e in tools if e.get("name") == "check_claim"), {})
    chk_out = str(chk.get("output", ""))
    signals = re.findall(r"'(VI_PHAM[A-Z_]*|DOI_[A-Z_]*|QUIZ_[A-Z_]*|CAU_MO_HO[A-Z_]*)'", chk_out)
    fake = re.search(r"'fake_codes': \[([^\]]*)\]", chk_out)
    fake = [x.strip(" '") for x in fake.group(1).split(",") if x.strip(" '")] if fake else []
    hint = re.search(r"'rule_hint': '([A-Z_]*)'", chk_out)
    m = model[0] if model else {}
    status = re.search(r"\[Trạng thái: ([^\]]*)\]", output or "")
    return {
        "claims": split_claims(text),
        "search_calls": len(searched), "segments_read": read,
        "signals": signals, "fake_codes": fake, "rule_hint": hint.group(1) if hint else "",
        "model": m.get("model", ""), "tokens_in": m.get("tokens_in", 0), "tokens_out": m.get("tokens_out", 0),
        "model_latency": m.get("latency_s", 0),
        "guardrail_notes": notes,
        "status": status.group(1) if status else "",
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):  # gọn log
        sys.stdout.write("[ui] %s\n" % (fmt % args))

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if path == "/api/info":
            return self._send(200, json.dumps({
                "provider": ai.MODEL_PROVIDER, "model": ai.MODEL_NAME or ai.MODEL_PROVIDER,
                "sources": load_sources()}, ensure_ascii=False))
        return self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/check":
            return self._send(404, json.dumps({"error": "not found"}))
        try:
            n = int(self.headers.get("Content-Length") or 0)
            text = (json.loads(self.rfile.read(n).decode("utf-8") or "{}").get("text") or "").strip()
        except Exception:
            return self._send(400, json.dumps({"error": "JSON không hợp lệ"}, ensure_ascii=False))
        if not text:
            return self._send(400, json.dumps({"error": "Chưa nhập nội dung"}, ensure_ascii=False))
        if len(text) > 4000:
            return self._send(400, json.dumps({"error": "Tối đa 4000 ký tự mỗi lần kiểm"}, ensure_ascii=False))
        with LOCK:
            tracing.begin("ui")
            try:
                out = answer(text)["output"]
                err = ""
            except Exception as e:  # noqa: BLE001
                out, err = "", "%s: %s" % (type(e).__name__, e)
            s, events = tracing.end()
        if err:
            return self._send(502, json.dumps({"error": err}, ensure_ascii=False))
        return self._send(200, json.dumps({
            "output": out, "models": s["models"], "model_calls": s["model_calls"], "tool_calls": s["tool_calls"],
            "tokens_in": s["tokens_in"], "tokens_out": s["tokens_out"],
            "pipeline": build_pipeline(text, events or [], out)}, ensure_ascii=False))


def main(argv):
    port = int(argv[argv.index("--port") + 1]) if "--port" in argv else 8765
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = "http://127.0.0.1:%d" % port
    print("Giao diện kiểm duyệt A3 đang chạy: %s  (model: %s · Ctrl+C để dừng)" % (url, ai.MODEL_NAME or ai.MODEL_PROVIDER))
    if "--no-browser" not in argv:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")


if __name__ == "__main__":
    main(sys.argv[1:])
