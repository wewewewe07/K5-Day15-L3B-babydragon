# AGENTS.md — hướng dẫn cho coding agent (Claude Code, Cursor, Codex…) làm việc trong repo này

> Ôn lại: ngày 12 · lab ngày 12. Nhóm sửa file này cho khớp bài của mình (thêm quy ước riêng, bỏ dòng không dùng).

## Repo này là gì

Repo nộp bài hackathon AI20K của nhóm: một bản chạy thử AI cho **một lát cắt** (xem `spec.md` §4), kèm bằng chứng, bộ câu thử và mô phỏng chi phí. Mọi câu trả lời phải chạy được bằng các lệnh dưới đây.

## Lệnh

```
python run.py                    # chạy bản chạy thử
python run.py check              # kiểm eval/benchmark.csv + eval/metric_spec.yaml
python run.py eval --try         # thử 3 câu đầu
python run.py eval               # chạy cả bộ → eval/run-N.csv + traces/run-N.jsonl
python run.py score eval/run-N.csv
python run.py simulate --try     # thử mô phỏng chi phí 10 phiên
python run.py simulate           # mô phỏng chi phí → cost/simulate-N.csv
```

Khung chỉ dùng thư viện chuẩn của Python. Thêm thư viện thì ghi vào `requirements.txt`.

## Cấu trúc code

| File | Ai sửa | Hợp đồng |
|---|---|---|
| `codebase/agent.py` | nhóm | `answer(text) -> {"output": str}` — luồng chính, đúng hình dạng ở `spec.md` §4 |
| `codebase/ai.py` | nhóm | `call_model(system, user) -> {"text", "model", "tokens_in", "tokens_out"}`, giữ `@model_call`. Token lấy từ `usage` của API, không ước lượng |
| `codebase/tools.py` | nhóm | mỗi công cụ một hàm có `@tool`, docstring: tên · input · output · có tác động ra ngoài không |
| `codebase/tracing.py`, `eval/run_eval.py`, `cost/simulate.py`, `run.py` | **khung — không sửa** | ghi trace, chạy bộ câu thử, mô phỏng chi phí |

## Luật — agent KHÔNG được làm

- Không commit `.env`, API key, dữ liệu cá nhân thật, nguyên file data BTC cấp.
- Không sửa `eval/run-*.csv`, `cost/simulate-*.csv`, `traces/*` đã chạy (trừ điền cột `pass`, `ghi_chu`).
- Không sửa chuẩn "đạt" (`spec.md` §7), `eval/metric_spec.yaml` sau CP2; không xoá câu thử trượt, không sửa `expected` cho khớp output.
- Không bịa người được phỏng vấn, trích dẫn, câu trả lời khảo sát, số liệu. Số không có nguồn thì ghi rõ *(tự ước tính)*.
- Công cụ có tác động ra ngoài (gửi tin, sửa dữ liệu, chấm điểm): chỉ tạo bản nháp chờ người duyệt.
- Không viết prompt "giấu" câu thử vào code (vd so khớp nguyên văn input của bộ câu thử).

## Quy ước của nhóm

- Ngôn ngữ trả lời người dùng: __
- Phong cách code / đặt tên: __
- Ai duyệt thay đổi do agent tạo trước khi commit: __
