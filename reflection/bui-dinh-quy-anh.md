# Reflection — Bùi Đình Quý Anh

- Nhóm: babydragon · Lớp: L3B · Track: A (EdTech) · Mã học viên: 2A202603969
- Lát cắt của nhóm: bot hỗ trợ giảng viên rà kịch bản và quiz bài giảng, đối chiếu từng câu với đoạn nguồn của khoá, gắn 1 trong 5 nhãn (`KHOP_NGUON`, `SAI_MAU_THUAN`, `LOI_CAU_HOI`, `THIEU_NGUON`, `TU_CHOI`) rồi chờ giảng viên duyệt, không tự xuất bản.

## 1. Vai trò + phần mình làm (trỏ tới file / commit)

Vai trò trong `TEAMS.md`: **Thành viên**, phụ trách bằng chứng pain, bộ câu thử và tiêu chí đánh giá (`evidence/`, `eval/benchmark.csv`, `eval/metric_spec.yaml`). Phần mình làm theo từng mốc:

- **CP2 — chốt định nghĩa "tốt"** (`2964488`):
  - Làm rõ chuẩn đạt trong `eval/metric_spec.yaml` và `spec.md` §7: câu sai nghiêm trọng là B06–B09 và B15, không câu nào trong số này được phán thành `KHOP_NGUON`.
  - Thống nhất bộ nhãn và các con số giữa `canvas.md`, `spec.md` và `evidence/summary.md` (số 9/15). Số nào nhóm tự ước tính thì đánh dấu *(tự ước tính)*.
  - Ghi rõ giới hạn của data preclass. Sửa lỗi đọc file UTF-8 trong `evidence/count.py` để script đếm chạy được trên Windows.
- **CP3 — nối model thật** (`deb8c49`, `1300240`):
  - Sửa `codebase/ai.py` để gọi `google/gemini-2.5-flash` qua OpenRouter, token lấy từ `usage` của API.
  - Chạy lượt 1 đạt 24/24 (`eval/run-1.csv`, `traces/run-1.jsonl`), cập nhật `eval/report.md` và `eval/README.md`.
  - Quay video demo 30 giây gọi AI thật, gắn link vào README.
- **CP4 — một lần cải tiến + đo lại** (`668f0a3`):
  - Viết bộ chịu tải `tests/stress_cases.csv` (27 câu) và script chấm tự động `tests/run_stress.py`, vì bộ chính thức đã đạt 100% nên không còn câu trượt để học.
  - Làm bot v2 trong `codebase/agent.py` và `codebase/tools.py`: tách câu bằng code (`split_claims`), tra nguồn theo từng câu, model gắn nhãn từng câu, code tính nhãn tổng = nhãn nặng nhất, code khoá `TU_CHOI` khi gặp injection hoặc yêu cầu đòi dữ liệu nhạy cảm.
  - Chạy lượt 2–4 trên 3 model (`eval/run-2.csv` … `run-4.csv`) để chọn model bằng số. Viết phần lỗi lượt 1 và phần cải tiến trong `eval/report.md`.
  - Cùng Ninh cập nhật số liệu cho `cost/cost-estimate.md` và slide trang 5–7.
- **Hoàn thiện repo** (`2af3fdc`, `7e32f15`, `60f497a`):
  - Rút gọn README, vẽ lại sơ đồ `spec.md` §4 cho khớp bot v2, thêm quy ước nhóm vào `AGENTS.md`.
  - Ghi cấu hình model vào `.env.example`.
  - Ghi lượt chạy thử nội bộ bằng model thật vào `validation/log.md`: đoạn nháp 2 câu ra đúng nhãn, chạy lại 51/51.
- **Giao diện web** `ui/` (`a441997`, `57641ca`, `745063d`):
  - Chạy bằng `python ui/server.py`. Hiển thị luồng 5 bước lấy từ trace, trích nguyên văn đoạn nguồn, nhãn từng câu và chi phí mỗi lượt.
  - Dùng bảng màu nhãn an toàn cho người mù màu.
- Thay tên trong tài liệu và slide thành tên đầy đủ (`668ed34`, `dccb7ad`).

## 2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI)

Công cụ: **Claude Code** (coding agent), làm việc theo luật trong `AGENTS.md`. Khai chi tiết ở `docs/ai-usage.md`.

- **Việc giao cho AI:**
  - Viết code bot v2 (`agent.py`, `tools.py`) và timeout/retry trong `ai.py`.
  - Sửa prompt hệ thống: định nghĩa 5 nhãn, cách xử lý quiz và mã nguồn giả, gắn nhãn từng câu.
  - Viết nháp 27 câu chịu tải.
  - Đề xuất cột `pass` và `ghi_chu` cho `run-1` … `run-4`.
  - Soạn nháp `eval/report.md`, `spec.md` §7–§10, `cost/cost-estimate.md` và code giao diện `ui/`.
- **Cách mình kiểm:**
  - Trước mỗi commit, chạy `python run.py check`, `python run.py eval --try` và `python tests/run_stress.py --all`, điểm không được lùi.
  - Đọc từng output trong `eval/run-*.csv`.
  - Mọi con số trong report và slide phải truy được về `eval/run-*.csv` hoặc `cost/simulate-*.csv`.
- **Chỗ phải sửa lại output AI:**
  - *Luật khoá `TU_CHOI` quá rộng:* bản đầu AI viết khoá theo từ khoá ("API key", "mật khẩu"…). Kết quả là câu B18, một câu kịch bản chỉ *nhắc tới* việc "không được để lộ API key", bị khoá nhầm, chạy trọn bộ còn 49/50. Mình đổi luật thành chỉ khoá khi có **động từ đòi hỏi** (in ra, cho tôi, gửi, print…), chạy lại được 50/50 rồi mới chạy lượt 2.
  - *Hàm tách câu:* bản đầu cắt các lựa chọn quiz A./B./C. thành câu riêng, làm mất ngữ cảnh câu hỏi. Mình yêu cầu giữ cả khối quiz thành một đơn vị và thêm câu S27 (kịch bản có quiz xen giữa) để kiểm.
  - *Chấm `pass`:* AI chỉ đề xuất, mình kiểm tay đủ 24/24 câu mỗi lượt. Câu sát ngưỡng (B13) mình ghi rõ lý do trong `ghi_chu`.
  - *Văn bản:* AI hay viết chung chung hoặc thêm số không có nguồn. Mình xoá những số đó hoặc đánh dấu *(tự ước tính)*.
- **Không dùng AI để:** tạo người được phỏng vấn, trích dẫn hay câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`); sửa `expected` hay chuẩn đạt cho khớp output.
- **Rút ra:** AI viết code và nháp rất nhanh, nhưng nó không tự biết đâu là "đúng" với người dùng. Chuẩn đạt, bộ câu thử và việc chạy lại để kiểm vẫn phải do mình làm. Mình phải hiểu từng dòng code AI viết thì mới giải thích được và mới bắt được lỗi như B18.

## 3. Một câu thử trượt của nhóm và mình học được gì từ nó

**Câu S12** (bộ chịu tải, chạy trên bot v1, model `google/gemini-2.5-flash`):

- *Input:* "Workflow cố định phù hợp khi các bước đã biết trước. Theo khảo sát của Gartner năm 2025, 87% doanh nghiệp đã chuyển sang Multi-Agent."
- *Output bot v1:* `KHOP_NGUON [SRC-D08-M1-01]`, kèm giải thích rằng câu đầu khớp nguồn.
- *Vì sao sai:* bot chỉ đối chiếu câu đầu. Số liệu "Gartner 87%" không có trong nguồn nhưng bị bỏ qua, nên cả đoạn được cho qua. Đây là kiểu bỏ sót lỗi (False Negative) mà `metric_spec.yaml` đặt ưu tiên số 1 và giảng viên trong phỏng vấn sợ nhất: khẳng định bịa lọt xuống hơn 700 học viên.
- *Đã sửa (bot v2):* tách câu bằng code, tra nguồn và gắn nhãn từng câu, code lấy nhãn nặng nhất làm nhãn tổng. Vẫn chỉ 1 lời gọi model mỗi lượt, token vào tăng khoảng 14% (1.240 → 1.416 / câu). Kết quả: nhóm lỗi "kịch bản nhiều câu" từ 2/3 lên 3/3, bộ chịu tải từ 21/26 lên 26/26, bộ chính thức vẫn 24/24, không vỡ câu nào.

**Mình học được:**

1. **Đạt 100% chưa chắc đã tốt.** Bộ chính thức do nhóm tự viết, mỗi câu một khẳng định, câu chữ bám sát nguồn, nên quá dễ. Lỗi thật chỉ lộ ra khi thử đúng dạng đầu vào người dùng đưa: cả đoạn kịch bản 30–40 câu (P1–P3), không phải từng câu lẻ.
2. **Việc gì kiểm chắc chắn được thì giao cho code.** Tách câu, gộp nhãn nặng nhất, kiểm mã nguồn có tồn tại, khoá `TU_CHOI` đều là phép kiểm tất định. Để model tự quyết những việc này thì nó có thể "quên" một câu.
3. **Sửa một lỗi có thể làm vỡ chỗ khác.** Lần sửa này kéo theo B18 bị khoá nhầm, nên sau mỗi thay đổi phải chạy lại trọn bộ chứ không chỉ chạy câu vừa sửa.
4. **Phải trung thực về giới hạn.** Bộ chịu tải được viết *sau khi* đã thấy lỗi, nên không phải bộ giữ riêng (held-out). Nếu có thêm thời gian, mình muốn lấy khoảng 20 đoạn kịch bản thật của khoá làm held-out, chấm tay mù, và đo thời gian duyệt có / không có bot với 2–3 giảng viên.
