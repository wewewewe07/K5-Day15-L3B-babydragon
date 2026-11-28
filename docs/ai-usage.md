# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Coding agent (Claude Code) | Viết `codebase/agent.py`, `tools.py` bản v2 (tách câu, tra nguồn từng câu, gộp nhãn nặng nhất, guardrail khoá `TU_CHOI`), timeout/retry trong `ai.py` | Bùi Đình Quý Anh chạy lại `run.py eval` + bộ chịu tải `tests/run_stress.py` trước khi commit, đọc từng output | Bùi Đình Quý Anh |
| Prompt / thiết kế lời gọi mô hình | Coding agent (Claude Code) | Sửa prompt hệ thống (định nghĩa 5 nhãn, quiz, mã giả, gắn nhãn từng câu) | Đối chiếu với `spec.md` §4–§5 và kết quả bộ chịu tải (21/26 → 26/26) | Nguyễn Thanh Tùng · Bùi Đình Quý Anh |
| Đào data (viết script đếm, gợi ý nhãn) | | | Kiểm tay __ dòng, khớp __ | |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Coding agent (Claude Code) | Viết bộ chịu tải `tests/stress_cases.csv` (27 câu, ngoài benchmark chính thức) | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ · benchmark chính thức 24 câu do nhóm viết | Bùi Đình Quý Anh |
| Sinh data `synthetic` (nếu có) | Coding agent (Claude Code) | Ghép 10 đoạn kịch bản × 7 câu từ benchmark cho mô phỏng chi phí (`cost/personas.yaml`) | Seed 2026 · kiểm tay 10/10 đoạn tách đúng 7 câu | Bùi Đình Quý Anh |
| Chấm cột `pass` bằng LLM (nếu có) | Coding agent (Claude Code) | Đề xuất cột `pass` + `ghi_chu` cho `run-1`…`run-4` theo `pass_criterion` | Kiểm tra thủ công 24/24 câu mỗi lượt; câu sát ngưỡng (B13) ghi rõ trong `ghi_chu` | Bùi Đình Quý Anh |
| Slide, văn bản | Coding agent (Claude Code) | Cập nhật `spec.md` §7–§8, §10, `eval/report.md`, `eval/README.md`, `cost/cost-estimate.md`, điền số slide trang 5–7 | Nhóm đọc lại trước khi nộp; mọi số truy về `eval/run-*.csv`, `cost/simulate-*.csv` | Bùi Đình Quý Anh · Trịnh Ngọc Ninh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
