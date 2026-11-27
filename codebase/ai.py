"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá:
        "text", "model", "tokens_in", "tokens_out"

Hỗ trợ sẵn:
- MODEL_PROVIDER=fake (mặc định cho CP2 khi chưa cấu hình .env)
- MODEL_PROVIDER=openai (hoặc các API tương thích OpenAI qua OPENAI_BASE_URL / OpenRouter / DeepSeek)
- MODEL_PROVIDER=gemini (Google Gemini API qua generativelanguage.googleapis.com)
- MODEL_PROVIDER=anthropic (Claude API)
- MODEL_PROVIDER=ollama (Local Ollama)
"""
import json
import os
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
OPENAI_BASE_URL = (os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1/chat/completions").strip()


def post_json(url, headers, body, timeout=60):
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"), method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP %d: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_openai(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(OPENAI_BASE_URL, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages, "temperature": 0.1})
    u = data.get("usage", {})
    return {
        "text": data["choices"][0]["message"]["content"],
        "tokens_in": u.get("prompt_tokens", 0),
        "tokens_out": u.get("completion_tokens", 0),
    }


def call_claude(system, user):
    url = "https://api.anthropic.com/v1/messages"
    data = post_json(url,
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data.get("usage", {})
    return {"text": text, "tokens_in": u.get("input_tokens", 0), "tokens_out": u.get("output_tokens", 0)}


def call_gemini(system, user):
    model_id = MODEL_NAME or "gemini-2.5-flash"
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (model_id, API_KEY)
    payload = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0.1},
    }
    if system:
        payload["systemInstruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {}, payload)
    candidates = data.get("candidates", [])
    parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
    text = "".join(p.get("text", "") for p in parts)
    u = data.get("usageMetadata", {})
    tok_in = int(u.get("promptTokenCount", 0))
    tok_out = int(u.get("candidatesTokenCount", 0)) + int(u.get("thoughtsTokenCount", 0))
    return {"text": text, "tokens_in": tok_in, "tokens_out": tok_out}


def call_ollama(system, user):
    url = "http://localhost:11434/api/chat"
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(url, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {
        "text": data["message"]["content"],
        "tokens_in": data.get("prompt_eval_count", 0),
        "tokens_out": data.get("eval_count", 0),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {
            "text": "[câu trả lời giả — chưa nối model] " + last[:80],
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }
    if MODEL_PROVIDER in ("openai", "openrouter", "deepseek"):
        r = call_openai(system, user)
    elif MODEL_PROVIDER == "anthropic":
        r = call_claude(system, user)
    elif MODEL_PROVIDER in ("gemini", "google"):
        r = call_gemini(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        raise NotImplementedError(
            "Chưa hỗ trợ MODEL_PROVIDER=%s trong codebase/ai.py — dùng openai, gemini, anthropic, hoặc ollama."
            % MODEL_PROVIDER
        )
    return {
        "text": r["text"],
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
