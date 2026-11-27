# Data card — dữ liệu bản chạy thử dùng (Track A3 · Kiểm duyệt bài giảng & câu hỏi AI)

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.

## Dataset 1 · Kho đoạn nguồn kiến thức chuẩn của khoá (`data/course_sources.json`)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | Làm nguồn sự thật (ground-truth knowledge base) cho các công cụ `search_sources(query)`, `get_segment(code)` và `check_claim(claim, sources)` trong bản chạy thử A3, đồng thời làm căn cứ chấm cho bộ câu thử `eval/benchmark.csv`. |
| **Từ đâu** | Tổng hợp và viết lại ngắn gọn các nguyên tắc cốt lõi của 15 ngày học Giai đoạn 1 khoá AI20K (tham chiếu từ `01-challenge-brief.md`, `02-guide.md` phụ lục Bản đồ 15 ngày, và `03-rubric.md`). **Không commit nguyên văn slide/transcript bản quyền của khoá** theo đúng Luật dùng dữ liệu mục 4. |
| **Xử lý những bước gì** | (1) Chia nhỏ kiến thức theo từng Ngày học (`Day01` → `Day13`) và Module; (2) Gán mã đoạn định danh duy nhất theo chuẩn `SRC-D<Ngày>-M<Module>-<Số>` (ví dụ `SRC-D05-M1-01`); (3) Kiểm tra tay 100% các mệnh đề và con số trong từng đoạn. |
| **Số dòng / số đoạn** | **12 đoạn nguồn chuẩn** (`SRC-D01-M1-01` đến `SRC-D13-M1-01`), bao phủ 12 chủ đề trọng tâm của khoá học. |
| **Phiên bản / ngày lấy** | `v1.0` — tạo ngày `27/11/2026` trước mốc CP2. |
| **Nhãn** | Nội dung kiến thức thật của khoá (đã biên tập thành đoạn trích ngắn có mã đoạn). |
| **Giới hạn** | Chỉ chứa 12 đoạn nguồn đại diện của khoá để chạy bản thử nghiệm trong 10 giờ hackathon (chưa chứa toàn bộ hàng trăm trang transcript của 15 ngày học). Do đó, mọi khẳng định thuộc chủ đề ngoài 12 đoạn này sẽ được hệ thống đánh dấu là `THIEU_NGUON` theo đúng thiết kế G10. |

---

## Dataset 2 · Nhật ký hành vi học tập thật trên trang Pre-class (`data/preclass/` của BTC)

| Thuộc tính | Chi tiết |
|---|---|
| **Dùng để làm gì** | (1) **Đào bằng chứng pain** (`evidence/data-mining.md` & `evidence/count.py`); (2) Lấy bối cảnh thực tế về các bài giảng bị `missing_context = True` và các `kc_code` học viên trả lời sai lần đầu cao nhất (`ai_product_canvas`, `agentic_fit_scoring_decision`, `react_reasoning_acting_pattern`...) để thiết kế các câu thử có `source = data_that:` trong `eval/benchmark.csv`. |
| **Từ đâu** | Bộ dữ liệu thật đã ẩn danh do BTC cấp trong thư mục `data/preclass/` của repo đề (`events.csv`, `chat.csv`, `answers.csv`, `learners.csv`). |
| **Xử lý những bước gì** | Viết script `evidence/count.py` đọc trực tiếp từ thư mục đề (không copy nguyên file CSV gốc vào repo nhóm), lọc theo `type == "agent_replied"`, `type == "video_seeked"`, và `nguon == "pre_post_post" & lan_thu == 1`. |
| **Số dòng / số đoạn** | `107.709` dòng sự kiện (`events.csv`), `1.260` lượt hỏi đáp (`chat.csv`), `3.776` lượt trả lời (`answers.csv`) trên `436` học viên có hoạt động (`05/11/2026` → `25/11/2026`). |
| **Phiên bản / ngày lấy** | Bản chính thức BTC phát ngày `27/11/2026`. |
| **Nhãn** | **Dữ liệu thật** (đã ẩn danh bởi BTC). |
| **Giới hạn** | Bản xuất của BTC không giữ nội dung chữ (`text`) của câu hỏi/trả lời để bảo vệ danh tính học viên, chỉ giữ mã bài (`transcript`, `kc_code`), độ dài ký tự và các cờ trạng thái (`missing_context`, `moc_trich_dan`, `was_correct`). |
