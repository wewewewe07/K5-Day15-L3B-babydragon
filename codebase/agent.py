"""Luồng chính của bản chạy thử — NHÓM VIẾT. Điền ở guide bước 3.2.

`python run.py`, `python run.py eval` và `python run.py simulate` đều gọi answer(text).

Hợp đồng:
    answer(text: str) -> dict có khoá "output" (str): kết quả đưa cho người dùng.
    Token, tên model, số lần gọi model / công cụ: khung tự đếm qua call_model và @tool — không cần trả.
    Bộ chạy gửi NGUYÊN ô input của câu thử vào text. Dữ liệu nền (bài học, thông báo, lịch…)
    do luồng của nhóm tự đọc qua công cụ trong tools.py.

Hình dạng: đúng như sơ đồ ở spec.md §4 (guide bước 2.2) — workflow cố định, một agent, hay nhiều agent.
Khung dưới đây là một workflow 2 bước VÍ DỤ, chỉ để luồng chạy hết từ trước CP2. Thay bằng luồng của nhóm.
Nếu viết vòng lặp agent (AI tự chọn bước tiếp): đặt giới hạn MAX_STEPS và ghi lý do dừng bằng note("dừng: …").
"""
from ai import call_model
from tools import search_example
from tracing import note  # noqa: F401

SYSTEM = ""     # NHÓM VIẾT: hướng dẫn hệ thống cho model (vai trò, phạm vi, khi nào nói "không có")
MAX_STEPS = 5   # dùng khi viết vòng lặp agent


def answer(text: str) -> dict:
    # Bước 1 (ví dụ): lấy căn cứ từ dữ liệu / công cụ của bài toán
    found = search_example(text)
    context = "\n".join("[%s] %s" % (p["code"], p["text"]) for p in found)
    # Bước 2 (ví dụ): model quyết định dựa trên căn cứ
    reply = call_model(SYSTEM, "Căn cứ:\n%s\n\nĐầu vào của người dùng:\n%s" % (context, text))
    return {"output": reply["text"]}
