# Nối model vào `codebase/ai.py`

> Làm ở guide bước 3.3. **Nên xong tối Thứ Sáu 27/11 trước khi ngủ** (sáng Thứ Bảy 28/11 không có lớp). Kẹt quá 20 phút thì hỏi ngay.

Mục tiêu: `call_model()` trong `codebase/ai.py` gọi model thật và trả về câu trả lời kèm **số token** đo được. Prompt và luồng là phần nhóm tự viết trong `codebase/agent.py`. File này chỉ lo phần kết nối.

Ba ví dụ dưới đây (OpenAI, Claude, Ollama) **đã chạy với key thật ngày 25/11/2026**: chép vào là chạy.

## 1. Điền `.env`

Chép `.env.example` thành `.env`, điền 3 dòng. Ví dụ:

```
MODEL_PROVIDER=openai
MODEL_NAME=gpt-5.4-nano
API_KEY=<key của nhóm, không dấu ngoặc kép>
```

- `MODEL_NAME` là **mã gọi API** của model, lấy ở trang tài liệu của nhà cung cấp.
- Chưa điền `MODEL_PROVIDER` thì `ai.py` chạy **chế độ giả** (câu giả, token 0). Dùng được cho bản khung trước CP2, nhưng `run.py eval` và `run.py simulate` không tính lượt đó.
- `.env` đã có trong `.gitignore`. **Không commit key.**

## 2. Chép code vào `codebase/ai.py`

Giữ nguyên phần đầu file (`load_env`, các biến) và nhánh `fake`.
1. Thêm 3 dòng `import` lên đầu file.
2. Dán hàm `post_json`.
3. Thay phần thân sau nhánh fake của `call_model` bằng đoạn dưới.
4. Dán **một** hàm `call_…` đúng nhà cung cấp nhóm dùng.

```python
import json
import urllib.error
import urllib.request

SHOW_RAW = False   # đổi thành True để in nguyên phản hồi của API khi cần tìm tên trường


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


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":              # nhánh fake của khung — giữ nguyên 3 dòng này
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER == "openai":
        r = call_openai(system, user)
    elif MODEL_PROVIDER == "anthropic":
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        r = call_provider(system, user)       # nhà cung cấp khác: mục 2.4
    return {"text": r["text"], "model": MODEL_NAME,
            "tokens_in": int(r["tokens_in"]), "tokens_out": int(r["tokens_out"])}
```

Luồng trong `agent.py` gọi model bao nhiêu lần cũng được: `@model_call` tự ghi từng lần vào trace và tự cộng token.

Luồng gọi **hai model** (vd model rẻ phân loại, model mạnh trả lời): thêm tham số tên model vào `call_model` và trả đúng tên model đã gọi ở khoá `"model"` (không trả chung `MODEL_NAME`). `simulate` dựa vào tên này để tính mỗi model theo giá của nó.

### 2.1 OpenAI

```python
URL_OPENAI = "https://api.openai.com/v1/chat/completions"


def call_openai(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OPENAI, {"Authorization": "Bearer " + API_KEY},
                     {"model": MODEL_NAME, "messages": messages})
    u = data["usage"]
    return {"text": data["choices"][0]["message"]["content"],
            "tokens_in": u["prompt_tokens"], "tokens_out": u["completion_tokens"]}
```

Nhà cung cấp có API theo định dạng OpenAI (ví dụ DeepSeek) dùng lại được hàm này, chỉ đổi `URL_OPENAI` theo tài liệu của hãng.

### 2.2 Claude

```python
URL_CLAUDE = "https://api.anthropic.com/v1/messages"


def call_claude(system, user):
    data = post_json(URL_CLAUDE,
                     {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
                     {"model": MODEL_NAME, "max_tokens": 1024, "system": system or "",
                      "messages": [{"role": "user", "content": user}]})
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    u = data["usage"]
    return {"text": text, "tokens_in": u["input_tokens"], "tokens_out": u["output_tokens"]}
```

- Ví dụ mã model: `claude-haiku-5-5` (tên trong bảng giá là "Claude Haiku 5.5").
- Câu trả lời bị cụt thì tăng `max_tokens`.

### 2.3 Model chạy trên máy (Ollama)

```python
URL_OLLAMA = "http://localhost:11434/api/chat"


def call_ollama(system, user):
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    data = post_json(URL_OLLAMA, {}, {"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=300)
    return {"text": data["message"]["content"],
            "tokens_in": data.get("prompt_eval_count", 0), "tokens_out": data.get("eval_count", 0)}
```

- Không cần key.
- **Rất chậm trên laptop:** ví dụ `gemma4:12b` mất 43–165 giây mỗi câu trên máy Mac. Chỉ hợp để thử luồng, không đủ nhanh để chạy hết bộ câu thử và 50 phiên mô phỏng.

### 2.4 Nhà cung cấp khác (Gemini…)

1. Mở trang quickstart chính thức của hãng, chép ví dụ Python **ngắn nhất** gọi được 1 câu, dán vào hàm dưới.
2. Bật `SHOW_RAW = True`, hỏi thử 1 câu, rồi xem câu trả lời và số token nằm ở trường nào trong phản hồi.
3. Dùng thư viện (SDK) của hãng thì ghi tên gói vào `requirements.txt`.

```python
def call_provider(system, user):
    """Gọi đúng MỘT lần model. Trả về {"text": str, "tokens_in": int, "tokens_out": int}."""
    # 1. gọi model bằng API_KEY và MODEL_NAME (chép từ quickstart)
    # 2. lấy chữ trả lời + số token vào / ra từ phản hồi
    raise RuntimeError("Chưa điền: chép ví dụ quickstart vào call_provider()")
```

## 3. Thử

1. `python run.py` → gõ 1 câu → thấy câu trả lời thật và dòng `(model: … · token vào … / ra …)`.
2. `python run.py eval --try` → chạy 3 câu thử đầu, thấy "Nối model được" là xong.
3. `python run.py eval` → `eval/run-1.csv` + `traces/run-1.jsonl`.

## 4. Lỗi hay gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `HTTP 401` / `403` | Sai key hoặc `.env` chưa lưu. Mở `.env` kiểm key: không thừa dấu cách, không dấu ngoặc kép |
| `HTTP 400` | Sai tên model, sai tên trường, hoặc tài khoản hết credit (đọc lời báo lỗi in ra) |
| `HTTP 429`, chạy vài câu rồi lỗi hàng loạt | Bị giới hạn số lượt gọi. Chạy **sớm**, thêm `--wait 4` sau `eval` / `simulate` |
| `KeyError` ở `usage` hoặc tên trường | Bật `SHOW_RAW = True`, xem phản hồi thật, sửa tên trường |
| `eval` báo "chưa gọi model thật" | `.env` chưa có `MODEL_PROVIDER`, hoặc token đều bằng 0 |
| Một số câu lỗi giữa chừng | **Không sửa tay file kết quả.** Chạy lại `python run.py eval` thành lượt mới |

Lỡ lộ key (commit `.env`, dán lên kênh chung) thì **thu hồi key ngay** trên trang nhà cung cấp. Xoá file thôi là không đủ.

## 5. Đo trên model X, tính giá model Y

Chi phí tính từ token đo được khi chạy `python run.py simulate`. Nhóm có thể đo token bằng model đang dùng để build, rồi tính theo giá model định dùng khi ra sản phẩm thật (khai ≥2 mức model trong `cost/personas.yaml` mục `prices`). Ghi rõ trong `cost/cost-estimate.md`: "đo token trên model X, tính giá model Y". Lưu ý: mỗi hãng tách token khác nhau, nên số token giữa hai hãng có thể lệch.

Tiếng Việt: **luôn đo token thật**, không quy đổi từ số chữ.
