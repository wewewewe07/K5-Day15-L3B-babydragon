# Đào data — cách đếm và kết quả (Track A3 · Kiểm duyệt bài giảng & câu hỏi AI)

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Script đếm tái lập: `python evidence/count.py --data-dir ../data/preclass` (người khác chạy lại ra đúng 100% số trong bảng dưới).
> Repo chỉ chứa số đã tổng hợp và các mã dòng ví dụ đã ẩn danh — không chép lại nguyên file data BTC.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** Bộ `data/preclass/` do BTC cấp (`events.csv` 107.709 dòng, `chat.csv` 1.260 dòng, `answers.csv` 3.776 dòng, `learners.csv` 721 tài khoản / **436 học viên có hoạt động**), ghi nhận từ `05/11/2026` đến `25/11/2026` (Day 01 → Day 13).
- **Đếm gì & Mẫu số là gì:**
  1. **Tỷ lệ lượt bài giảng thiếu ngữ cảnh (`missing_context = True`):** Đếm các sự kiện `type == "agent_replied"` trong `events.csv` có trường JSON `missing_context` khác rỗng (`N = 1.245` lượt có trường này trên tổng 1.260 lượt `agent_replied`). Tử số `x` là số lượt `missing_context == True`.
  2. **Tỷ lệ lượt không dẫn được mốc trích dẫn trong bài giảng (`moc_trich_dan` rỗng `[]`):** Đếm trên tập sự kiện `agent_replied` có ghi nhận trường `moc_trich_dan` (`N = 604` lượt). Tử số `x` là số lượt `moc_trich_dan` rỗng (`[]`).
  3. **Tỷ lệ câu hỏi kiểm tra (`pre_post_post`) học viên trả lời sai ngay lần thử đầu tiên (`lan_thu == 1`):** Lọc `answers.csv` với `nguon == "pre_post_post"` và `lan_thu == 1` có chấm đúng/sai (`N = 1.968` lượt trả lời lần đầu). Nhóm theo từng ý kiến thức `kc_code` (lọc các `kc_code` có `N >= 15` lượt làm lần đầu) để tìm những đoạn bài giảng/câu hỏi làm học viên hiểu sai nhiều nhất.
  4. **Tần suất học viên phải tua lại video để tìm thông tin (`video_seeked`):** Đếm số học viên có sự kiện `type == "video_seeked"` trên mẫu số **N = 436 học viên có hoạt động** (không chia cho 721 tài khoản đăng ký để tránh sai mẫu số theo đúng lưu ý trong `data/preclass/README.md`).
- **Script kiểm chứng:** [evidence/count.py](count.py)

## 2. Đọc trước, đếm sau

Đã đọc 50 dòng đầu của `events.csv`, `chat.csv`, `answers.csv` cùng `column_dictionary.csv` và `event_types.csv`. Các *kiểu* hành vi thấy được liên quan trực tiếp đến chất lượng kịch bản bài giảng và câu hỏi tương tác (A3):
- Khi kịch bản bài giảng hoặc slide viết thiếu căn cứ / định nghĩa chưa rõ ở một đoạn video, học viên xem đến đó sẽ phải bấm hỏi trợ giảng AI dưới video (`channel = video_question`, chiếm 1.108/1.260 lượt chat) hoặc bôi đen chữ trên slide để hỏi (`slide_text_asked`: 433 lượt), và hệ thống gán cờ `missing_context = True`.
- Nhiều câu hỏi kiểm tra theo ý kiến thức (`kc_code`) có tỷ lệ học viên trả lời sai ngay lần đầu (`lan_thu = 1`) lên tới **50%–80%**, cho thấy độ khớp giữa nội dung giảng trong kịch bản và câu hỏi kiểm tra ở các ý kiến thức đó đang có điểm nghẽn lớn cần được rà soát trước khi xuất bản.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---:|---:|---|
| Lượt hỏi dưới bài giảng bị đánh dấu **thiếu ngữ cảnh trong bài** (`missing_context = True`) | **101 / 1.245** | **8,1%** | Tập trung cao nhất ở `Day01/d01-r1-v01.txt` (19 lượt) và `Day02/d02-r2-v01.txt` (10 lượt) |
| Lượt trả lời từ bài giảng **không dẫn ra được mốc giây trích dẫn nào** (`moc_trich_dan = []`) | **231 / 604** | **38,2%** | Trên 604 lượt `agent_replied` có log trường `moc_trich_dan`, hơn 1/3 không trỏ được về mốc nguồn trong bài |
| Lượt trả lời câu hỏi ôn tập (`pre_post_post`) **sai ngay lần thử đầu tiên** (`lan_thu = 1`) | **399 / 1.968** | **20,3%** | Trung bình 1/5 câu trả lời lần đầu sau khi xem bài bị sai |
| Ý kiến thức `ai_product_canvas` có học viên trả lời sai ở lần đầu (`lan_thu = 1`) | **12 / 15** | **80,0%** | Điểm nghẽn cao nhất trong các `kc_code` có ≥15 lượt trả lời lần đầu |
| Ý kiến thức `agentic_fit_scoring_decision` có học viên trả lời sai ở lần đầu (`lan_thu = 1`) | **12 / 20** | **60,0%** | Điểm nghẽn cao thứ 2 — ranh giới chọn Workflow hay Agent dễ gây nhầm nếu câu hỏi/lời giảng thiếu căn cứ rõ |
| Ý kiến thức `feedback_signal_types` và `react_reasoning_acting_pattern` sai lần đầu | **8/15** và **9/18** | **53,3%** và **50,0%** | Hơn một nửa học viên làm sai ngay lần đầu sau khi học đoạn bài tương ứng |

## 4. ≥5 ví dụ cụ thể (mã dòng đã ẩn danh từ `data/preclass/`)

1. **`ref_id = C00983`** (`transcript = Day01/d01-r1-v05.txt`, `channel = video_question`): Học viên đặt câu hỏi ngắn 29 ký tự ngay dưới video bài giảng Ngày 1, nhưng hệ thống ghi nhận `missing_context = True` và `moc_trich_dan = NaN` (bài giảng tại đoạn đó không đủ căn cứ ngữ cảnh để trích dẫn).
2. **`ref_id = C00992`** (`transcript = Day02/d02-r2-v01.txt`, `channel = video_question`): Học viên hỏi câu dài 34 ký tự dưới video Ngày 2 (`d02-r2-v01`), hệ thống trả lời 298 ký tự nhưng báo `missing_context = True` (thiếu ngữ cảnh gốc trong transcript).
3. **`ref_id = C00998`** (`transcript = Day02/d02-r2-v01.txt`, `channel = video_question`): Học viên hỏi câu chi tiết 91 ký tự ở cùng bài giảng `Day02/d02-r2-v01.txt`, tiếp tục bị `missing_context = True` — chỉ riêng file transcript `Day02/d02-r2-v01.txt` đã phát sinh **10 lượt** thiếu ngữ cảnh.
4. **`ref_id = C00676`** (`transcript = Day01/d01-r1-v01.txt`, `channel = video_question`): Học viên hỏi câu 48 ký tự, AI trả lời 359 ký tự nhưng `missing_context = True` — file transcript `Day01/d01-r1-v01.txt` đứng đầu toàn khoá với **19 lượt** thiếu ngữ cảnh.
5. **Nhóm câu hỏi thuộc `kc_code = ai_product_canvas` và `agentic_fit_scoring_decision` trong `answers.csv` (`nguon = pre_post_post`, `lan_thu = 1`):** Có lần lượt **12/15 (80,0%)** và **12/20 (60,0%)** lượt học viên trả lời sai ngay lần đầu sau khi xem bài giảng, phản ánh khoảng vênh giữa lời giảng trong kịch bản và câu hỏi kiểm tra tương tác.

## 5. Giới hạn của data

- **Giới hạn:** `data/preclass/` đã ẩn danh toàn bộ nội dung chữ (`text`) nên cho biết chính xác **file transcript nào (`Day01/d01-r1-v01.txt`, `Day02/d02-r2-v01.txt`...) và ý kiến thức nào (`ai_product_canvas`, `agentic_fit_scoring_decision`...) đang bị thiếu ngữ cảnh hoặc làm học viên sai nhiều**, nhưng không chứa nguyên văn câu kịch bản AI sinh lúc chưa duyệt.
- **Kiểm lại bằng phỏng vấn & khảo sát:** Nhóm thực hiện phỏng vấn trực tiếp người làm nội dung/TA/Lab Coach và khảo sát 2 nhánh ([evidence/survey/TEMPLATE.md](survey/TEMPLATE.md)) để lấy nguyên văn các ví dụ lỗi kịch bản / câu hỏi tương tác ngoài đời thực.
