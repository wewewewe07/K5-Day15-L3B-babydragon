# Tổng hợp bằng chứng pain (Track A3 · Kiểm duyệt bài giảng & câu hỏi tương tác bằng AI)

> Điền ở guide bước 1.2, cập nhật tại **CP2 19:30 Thứ Sáu 27/11** và chốt hoàn chỉnh trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1 (14 điểm).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| **Đào data** (`x/N`, `%`, cách đếm chạy lại được bằng `evidence/count.py`, ≥5 ví dụ mã dòng thật) | ☑ **ĐẠT** | `evidence/data-mining.md` · `evidence/count.py` |
| **Khảo sát & Phỏng vấn phân nhánh** (Nhánh 1: Giảng viên / Lab Coach · Nhánh 2: Học viên L3) | ☑ **ĐÃ THU ĐƯỢC 10 PHẢN HỒI THẬT (3 GV/Lab Coach + 7 Học viên, đang tiếp tục mở form tới CP3)** | `evidence/survey/questions.md` · `evidence/interviews/` |

## 2. Số chính

- **Đào data (`data/preclass/` — 107.709 dòng sự kiện, 436 học viên có hoạt động):**
  - **101 / 1.245 lượt (8,1%)** hỏi dưới bài giảng bị hệ thống đánh dấu **`missing_context = True`** (nội dung bài giảng tại đoạn đó thiếu ngữ cảnh để giải đáp, cao nhất ở `Day01/d01-r1-v01.txt` với 19 lượt và `Day02/d02-r2-v01.txt` với 10 lượt).
  - **231 / 604 lượt (38,2%)** câu trả lời trên bài giảng **không dẫn ra được mốc trích dẫn nào** trong bài (`moc_trich_dan = []`).
  - **232 / 436 học viên có hoạt động (53,2%)** có tổng cộng **4.322 lượt tua video (`video_seeked`)** *(tua video có thể là hành vi học bình thường; data không cho biết lý do tua)*.
  - **399 / 1.968 lượt (20,3%)** học viên trả lời sai ngay lần thử đầu tiên (`lan_thu = 1`) ở bài kiểm tra `pre_post_post`; cá biệt ở các ý kiến thức mà lời giảng/câu hỏi chưa khớp rõ như `ai_product_canvas` sai **12/15 (80,0%)**, `agentic_fit_scoring_decision` sai **12/20 (60,0%)**, `feedback_signal_types` sai **8/15 (53,3%)**, `react_reasoning_acting_pattern` sai **9/18 (50,0%)**.
- **Phản hồi từ phía Người dạy / Kiểm duyệt (Giảng viên & Lab Coach — `n = 3` phản hồi đầu tiên, `n` nhỏ không ghi %):**
  - **3/3 người** chỉ ra lỗi trực tiếp ở chất lượng nội dung do AI sinh ra: **sinh sai nội dung / bịa nội dung ("quá bịp")** và **hiển thị công thức không rõ nét/sai định dạng**.
- **Phản hồi từ phía Người tiếp thu & Tự học bằng AI (Học viên L3 — 7 phản hồi chi tiết đầu tiên, đang tiếp tục gom đủ `N ≥ 20` trước CP3):**
  - Chỉ ra **3 nhóm lỗi cốt lõi** của nội dung/câu hỏi bài giảng do AI sinh khi chưa được kiểm chứng chặt với nguồn:
    1. **Câu hỏi tương tác hỏi kiến thức không có trong slide/bài giảng nguồn** (VD: hỏi về *Google PAIR* hoặc *Lost in the Middle ở LLM* nhưng slide bài đó chưa đề cập, khiến học viên phải tự tra cứu bên ngoài).
    2. **Nội dung/đáp án câu hỏi do AI sinh khó hiểu, thiếu tường minh vì chưa được kiểm chứng**, làm học viên phải **tua lại video khoảng 5 phút** và suy nghĩ mới trả lời được.
    3. **Bản tóm tắt AI cắt mất điều kiện ngoại lệ quan trọng** (VD: chỉ ghi ngắn gọn *"áp dụng quy tắc ba điểm"* mà bỏ qua điều kiện ngoại lệ trong bài đọc gốc, dẫn đến ví dụ đi kèm cho kết quả ngược lại, buộc người học phải mở lại tài liệu gốc đọc phần lưu ý chi tiết bên dưới).

### Bảng tổng hợp phản hồi từ Giảng viên / Lab Coach (Nhánh Người dạy)

| Mã | Vai | Gặp pain? | Vấn đề cốt lõi gặp phải khi duyệt/xem nội dung AI sinh | Trích dẫn nguyên văn |
|---|---|---|---|---|
| **P1 (GV/LC-1)** | Giảng viên / Lab Coach | **Có** | AI bịa đặt khẳng định không có căn cứ thật trong tài liệu nguồn | *"Nội dung quá bịp"* |
| **P2 (GV/LC-2)** | Giảng viên / Lab Coach | **Có** | AI sinh sai kiến thức chuyên môn so với bài gốc | *"sinh sai nội dung"* |
| **P3 (GV/LC-3)** | Giảng viên / Lab Coach | **Có** | Công thức toán/kỹ thuật AI sinh hoặc dựng lên slide bị lỗi, không rõ nét | *"Công thức ghi xấu k rõ nét"* |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, đã bỏ tên cá nhân)

1. **"Nội dung trên Pre-class nhiều khi đọc rất khó hiểu bởi vì cũng được bởi AI. Mình phải tua lại khoảng 5 phút, sau đó nghĩ một lúc thì mới trả lời được. Đáp án của câu đó chưa được tường minh, khả năng do nội dung chưa được kiểm chứng và chất lượng chưa tốt"** — *Phản hồi khảo sát Học viên L3 #HV01 (Nhánh Người tiếp thu)*.
2. **"gặp câu hỏi về google PAIR nhưng không tìm thấy slide chứa nội dung đó"** — *Phản hồi khảo sát Học viên L3 #HV03 (Nhánh Người tiếp thu)*.
3. **"Tuần trước, bản tóm tắt AI chỉ ghi ngắn gọn 'áp dụng quy tắc ba điểm' nhưng không nêu rõ điều kiện ngoại lệ, khiến mình không hiểu tại sao ví dụ đi kèm lại cho kết quả ngược lại. Mình đã phải mở lại bài đọc gốc để xem phần lưu ý chi tiết bên dưới thì mới nắm được cách giải đúng."** — *Phản hồi khảo sát Học viên L3 #HV07 (Nhánh Người tiếp thu)*.
4. **"Nội dung quá bịp"** & **"sinh sai nội dung"** — *Phản hồi khảo sát Giảng viên / Lab Coach #GVLC01 & #GVLC02 (Nhánh Người dạy)*.
5. **"nguyên nhân dẫn đến Lost the Middle ở LLM"** & **"chủ yếu là các thuật ngữ mới mình cần phải tra ngoài"** — *Phản hồi khảo sát Học viên L3 #HV05 & #HV06 về các câu hỏi/khái niệm xuất hiện trong câu hỏi nhưng thiếu giải thích trong bài giảng*.
6. **Mã dòng dữ liệu thật `ref_id = C00676`, `C00983` (`Day01/d01-r1-v01.txt`, `v05.txt`) và `C00992`, `C00998` (`Day02/d02-r2-v01.txt`):** Ghi nhận tổng cộng **101/1.245 lượt (8,1%)** câu hỏi dưới bài giảng bị `missing_context = True` và **231/604 lượt (38,2%)** không có `moc_trich_dan`.

## 4. Các nguồn có khớp nhau không (Kiểm chéo Data ↔ Người dạy ↔ Người học)

**Các nguồn cùng chỉ về một hướng, nhưng mức độ chắc khác nhau:**
- **Góc Người dạy (Giảng viên / Lab Coach)** xác nhận nguyên nhân gốc là model AI *"sinh sai nội dung"* và *"nội dung quá bịp"* (ảo giác trôi chảy).
- **Góc Người học (Học viên L3)** chỉ ra chính xác hậu quả khi các câu khẳng định/câu hỏi chưa được kiểm chứng đó lọt lên trang Pre-class: (1) câu hỏi hỏi về *Google PAIR* hay *Lost in the Middle* nhưng **không có trong slide nguồn**; (2) bản tóm tắt AI **bỏ sót điều kiện ngoại lệ** (*"quy tắc ba điểm"*) làm ví dụ ra kết quả ngược lại; (3) đáp án câu hỏi thiếu tường minh khiến học viên **phải tua lại video khoảng 5 phút** và mở lại tài liệu gốc để kiểm tra.
- **Góc Dữ liệu log (`data/preclass/`) — tín hiệu phụ, không đo trực tiếp lỗi nội dung:** `missing_context` và `moc_trich_dan` là cờ của **câu trả lời trợ giảng AI**, không phải nhãn chất lượng kịch bản bài giảng; tua video không chứng minh học viên đang dò lỗi. Các số: **53,2% học viên (232/436 người)** phải tua lại video tổng cộng **4.322 lần**, **8,1% lượt hỏi (101/1.245)** rơi vào đoạn bài giảng thiếu ngữ cảnh (`missing_context = True`), và tỷ lệ làm sai câu hỏi lần đầu ở các chủ đề khó lên tới **50%–80%**.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **ĐÚNG và được làm sắc nét hơn** — Không chỉ dừng ở việc AI bịa thêm thông tin bên ngoài, phản hồi thực tế của người dùng chỉ ra 2 lỗi cực kỳ cụ thể mà bộ kiểm duyệt A3 phải bắt được:
1. **Câu hỏi tương tác hỏi khái niệm không nằm trong slide/tài liệu nguồn của bài đó** (như ca *Google PAIR* / *Lost in the Middle* → phải gắn nhãn `THIEU_NGUON`).
2. **Câu tóm tắt/khẳng định của AI cắt bỏ mất điều kiện ngoại lệ quan trọng trong tài liệu gốc** (như ca *"quy tắc ba điểm"* thiếu điều kiện ngoại lệ → phải gắn nhãn `SAI_MAU_THUAN` kèm trích dẫn đoạn lưu ý trong nguồn).

## Lịch thu thập tiếp (CP2 → CP3)

| Vai | Tiến độ tại CP2 (18:30 Thứ Sáu 27/11) | Mục tiêu trước CP3 (10:00 Thứ Bảy 28/11) |
|---|---|---|
| Giảng viên / Lab Coach (Nhánh Người dạy) | Đã thu 3 phản hồi (`GVLC01`–`GVLC03`) | Phỏng vấn sâu thêm chi tiết thời gian duyệt bài (`P1.md`–`P3.md`) |
| Học viên L3 (Nhánh Người tiếp thu) | Đã thu 7 phản hồi tự luận chi tiết (`HV01`–`HV07`) | Gom đủ `≥20` phiếu trong `evidence/survey/results.csv` |
