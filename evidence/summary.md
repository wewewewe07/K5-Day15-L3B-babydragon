# Tổng hợp bằng chứng pain (Track A3 · Kiểm duyệt bài giảng & câu hỏi tương tác bằng AI)

> Điền ở guide bước 1.2, hoàn thành đầy đủ cả 3 nguồn trước **CP2 / CP3**. Chấm ở rubric R1 (**14/14 điểm**).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| **Đào data** (`x/N`, `%`, cách đếm chạy lại được bằng `evidence/count.py`, ≥5 ví dụ mã dòng thật) | ☑ **ĐẠT** (107.709 dòng sự kiện, 436 học viên active) | `evidence/data-mining.md` · `evidence/count.py` |
| **Phỏng vấn & Hỏi sâu Nhánh Người dạy** (`≥3` người ngoài nhóm: 1 Giảng viên/Đội bài giảng + 2 TA/Key Coach/Lab Coach) | ☑ **ĐẠT** (`3/3` người, đủ 3 file `P1.md`–`P3.md`) | `evidence/interviews/P1.md`, `P2.md`, `P3.md` |
| **Khảo sát phân nhánh** (`≥20` người ngoài nhóm: **N = 24 người** gồm 3 Giảng viên/Coach & 21 Học viên L3) | ☑ **ĐẠT** (`N = 24 ≥ 20`, lưu đủ `questions.md` & `results.csv`) | `evidence/survey/questions.md` · `evidence/survey/results.csv` |

## 2. Số chính

### (a) Đào data (`data/preclass/` — N = 436 học viên có hoạt động)
- **101 / 1.245 lượt (8,1%)** hỏi dưới bài giảng bị hệ thống đánh dấu **`missing_context = True`** (nội dung bài giảng tại đoạn đó thiếu ngữ cảnh để giải đáp, cao nhất ở `Day01/d01-r1-v01.txt` với 19 lượt và `Day02/d02-r2-v01.txt` với 10 lượt).
- **231 / 604 lượt (38,2%)** câu trả lời trên bài giảng **không dẫn ra được mốc trích dẫn nào** trong bài (`moc_trich_dan = []`).
- **232 / 436 học viên có hoạt động (53,2%)** có tổng cộng **4.322 lượt tua video (`video_seeked`)** *(tua video có thể là hành vi học bình thường; data không cho biết lý do tua)*.
- **399 / 1.968 lượt (20,3%)** học viên trả lời sai ngay lần thử đầu tiên (`lan_thu = 1`) ở bài kiểm tra `pre_post_post`; cá biệt ở các ý kiến thức mà lời giảng/câu hỏi chưa khớp rõ như `ai_product_canvas` sai **12/15 (80,0%)**, `agentic_fit_scoring_decision` sai **12/20 (60,0%)**, `feedback_signal_types` sai **8/15 (53,3%)**, `react_reasoning_acting_pattern` sai **9/18 (50,0%)**.

### (b) Phỏng vấn & Khảo sát Nhánh Người dạy (`n = 3`: 1 Giảng viên/Đội sản xuất bài giảng + 2 TA/Key Coach/Lab Coach — `n` nhỏ không ghi %)
- **3/3 người** đều trực tiếp rà soát nội dung bài giảng / bộ câu hỏi do AI sinh trong tháng qua, với tần suất: **P1 = 3 bài/tháng**, **P2 = 10 bài/tháng**, **P3 = 15 bài/tháng** (trung bình ~9,3 bài/người/tháng).
- **Thời gian kiểm duyệt thủ công mỗi bài (Câu 4A):** **15–30 phút/bài** (với TA/Lab Coach `P2`, `P3`) và **30–60 phút/bài** (với Giảng viên/Đội sản xuất bài giảng `P1`).
- **Các lỗi phát hiện trong bản nháp AI sinh (Câu 5A):**
  - **2/3 người (`P1`, `P2`)** gặp lỗi *"Khẳng định trôi chảy nhưng không có trong tài liệu nguồn (AI tự đưa kiến thức ngoài vào)"* và *"Sai kiến thức tinh vi (đảo ngược điều kiện, lệch thuật ngữ chuẩn của khoá)"*.
  - **2/3 người (`P1`, `P3`)** gặp lỗi *"Câu hỏi lộ sẵn đáp án hoặc câu chữ mơ hồ, nhiều cách hiểu"*.
  - **1/3 người (`P1` - Đội bài giảng)** chỉ rõ: *"Không ghi rõ đoạn nào trong tài liệu gốc làm căn cứ nên rất tốn công tìm lại nguồn"*.

| Mã | Vai | Gặp pain? | Số bài rà soát / 1 tháng qua | Mỗi lần mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| **P1** | Giảng viên / Đội sản xuất bài giảng online | **Có** | 3 bài giảng | **30–60 phút** | Mở song song 2 cửa sổ đọc dò bằng mắt + `Ctrl+F` tìm từ khoá + nhờ AI khác kiểm lại |
| **P2** | TA / Key Coach / Lab Coach | **Có** | 10 bài / tài liệu | **15–30 phút** | Mở song song 2 cửa sổ đọc dò bằng mắt |
| **P3** | TA / Key Coach / Lab Coach | **Có** | 15 bài / bộ câu hỏi | **15–30 phút** | Chỉ đọc lướt theo trí nhớ chuyên môn (vì không đủ thời gian dò nguồn từng câu → dễ lọt lỗi) |

### (c) Khảo sát Nhánh Người tiếp thu (`N_total = 24` phiếu, trong đó `N_hv = 21` Học viên L3A/L3B)
- **18 / 21 học viên (85,7%)** gặp câu hỏi tương tác hoặc khẳng định trên Pre-class làm họ thấy mơ hồ / chưa được giảng rõ ở đoạn trước đó từ **2 đến 7 lần** chỉ trong 2 tuần gần đây (**trung bình 2,8 lần / học viên / 2 tuần**, tương đương **~5,6 lần / tháng**).
- **Các vấn đề cụ thể học viên gặp phải trên bài giảng/câu hỏi AI (`N = 21`):**
  - **12 / 21 học viên (57,1%)** gặp lỗi: *"Câu hỏi hỏi một ý chưa được giải thích hoặc thiếu ngữ cảnh trong đoạn bài giảng ngay trước đó"*.
  - **9 / 21 học viên (42,9%)** gặp lỗi: *"Lời giải thích hoặc thuật ngữ giữa các phần / giữa câu hỏi và video chưa khớp nhau"*.
  - **5 / 21 học viên (23,8%)** gặp lỗi: *"Khi hỏi trợ giảng AI dưới video, câu trả lời không chỉ rõ đoạn / mốc giây nào của bài giảng"*.
  - **3 / 21 học viên (14,3%)** gặp lỗi: *"Câu hỏi lộ đáp án trong câu dẫn hoặc quá mơ hồ, không rõ hỏi ý nào"*.
- **Cách học viên xoay xở & Thời gian mất thêm mỗi lần (`N = 21`):**
  - **16 / 21 học viên (76,2%)** phải tự mở tìm kiếm bên ngoài (ChatGPT/Google) và **12 / 21 học viên (57,1%)** phải **tua đi tua lại video** để tìm đúng đoạn nói về ý đó.
  - **15 / 21 học viên (71,4%)** mất từ **5 phút đến trên 30 phút** cho mỗi lần tự dò lại nguồn (cụ thể: 13 người mất `5–15 phút`, 1 người mất `15–30 phút`, 1 người mất `trên 30 phút`; 6 người mất `dưới 5 phút`).
- **Khi học viên tự dùng AI để tóm tắt bài giảng/tạo câu hỏi ôn tập (`N = 21`):**
  - **16 / 21 học viên (76,2%)** từng gặp tình trạng AI tự bịa ý ngoài bài hoặc trộn sai thuật ngữ của khoá (trong đó **6/21 = 28,6% thường xuyên gặp** và phải tự mở slide gốc dò lại; **10/21 = 47,6% thỉnh thoảng gặp**).

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn từ `results.csv` & `interviews/`, đã bỏ tên)

1. **"Nội dung quá bịp"** & **"sinh sai nội dung"** & **"Công thức ghi xấu k rõ nét"** — *P1 (Giảng viên / Đội sản xuất bài giảng, dòng 11 `results.csv`), P3 (TA / Lab Coach, dòng 10 `results.csv`), P2 (TA / Lab Coach, dòng 8 `results.csv`)*.
2. **"Nội dung trên Pre-class nhiều khi đọc rất khó hiểu bởi vì cũng được bởi AI. Mình phải tua lại khoảng 5 phút, sau đó nghĩ một lúc thì mới trả lời được. Đáp án của câu đó chưa được tường minh, khả năng do nội dung chưa được kiểm chứng và chất lượng chưa tốt"** — *Học viên L3 (dòng 14 `results.csv`)*.
3. **"Tuần trước, bản tóm tắt AI chỉ ghi ngắn gọn 'áp dụng quy tắc ba điểm' nhưng không nêu rõ điều kiện ngoại lệ, khiến mình không hiểu tại sao ví dụ đi kèm lại cho kết quả ngược lại. Mình đã phải mở lại bài đọc gốc để xem phần lưu ý chi tiết bên dưới thì mới nắm được cách giải đúng."** — *Học viên L3 (dòng 1 `results.csv`)*.
4. **"gặp câu hỏi về google PAIR nhưng không tìm thấy slide chứa nội dung đó"** & **"Lúc đó gặp câu hỏi nhưng không biết câu hỏi đến từ chương nào nên mới phải mò lại"** — *Học viên L3 (dòng 9 và dòng 23 `results.csv`)*.
5. **"nội dung do AI tạo bị lệch so với bài gốc khiến mình phải kiểm tra lại nguồn thông tin của bài giảng gốc"** — *Học viên L3 (dòng 15 `results.csv`)*.
6. **"AI sử dụng các thuật ngữ mà mình gặp lần đầu nên phải đụng AI để giải thích và khá tốn thời gian"** & **"Gặp các thuật ngữ tiếng anh chuyên ngành chưa rõ ý nghĩa"** — *Học viên L3 (dòng 17 và dòng 18 `results.csv`)*.

## 4. Các nguồn có khớp nhau không (Kiểm chéo Data ↔ Người dạy ↔ Người học)

**Các nguồn cùng chỉ về một hướng, nhưng mức độ chắc khác nhau:**
- **Góc Người dạy (Giảng viên / Lab Coach — `P1`..`P3`)** xác nhận nguyên nhân gốc ở khâu sản xuất: model AI *"sinh sai nội dung"*, *"nội dung quá bịp"* (ảo giác trôi chảy) và bản nháp không gắn mã đoạn nguồn nên người duyệt phải mở 2 cửa sổ dò mắt mất **15–60 phút/bài** (`P1`, `P2`), hoặc vì quá tải (15 bài/tháng như `P3`) nên chỉ *"đọc lướt theo trí nhớ chuyên môn"* khiến lỗi lọt qua.
- **Góc Người học (Học viên L3 — `21 học viên` trong `results.csv`)** chỉ ra chính xác hậu quả khi các câu khẳng định/câu hỏi chưa được kiểm chứng đó lọt lên trang Pre-class: **57,1% (12/21)** gặp câu hỏi hỏi ý chưa được giải thích/thiếu ngữ cảnh trong đoạn bài trước đó (như *Google PAIR* hay *Lost in the Middle*); **42,9% (9/21)** gặp lời giải thích hoặc thuật ngữ chưa khớp nhau; bản tóm tắt AI **bỏ sót điều kiện ngoại lệ** (*"quy tắc ba điểm"*); và **71,4% (15/21)** mất từ **5 đến >30 phút** mỗi lần phải tua lại video hoặc mở lại tài liệu gốc để kiểm tra.
- **Góc Dữ liệu log (`data/preclass/`) — tín hiệu phụ, không đo trực tiếp lỗi nội dung:** `missing_context` và `moc_trich_dan` là cờ của **câu trả lời trợ giảng AI**, không phải nhãn chất lượng kịch bản bài giảng; tua video không chứng minh học viên đang dò lỗi. Các số: **53,2% học viên (232/436 người)** có tổng cộng **4.322 lần** tua video, **8,1% lượt hỏi (101/1.245)** rơi vào đoạn bài giảng thiếu ngữ cảnh (`missing_context = True`), và tỷ lệ làm sai câu hỏi lần đầu ở các chủ đề khó lên tới **50%–80%**.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **ĐÚNG** — Đã chứng minh bằng cả 3 nguồn độc lập đạt ngưỡng. Chỗ nghẽn lớn nhất của sản xuất bài giảng bằng AI (A3) nằm ở việc thiếu một luồng đối chiếu tự động từng câu khẳng định/câu hỏi với đoạn nguồn chính thức của khoá (`[SRC-...]`) để bắt 4 loại lỗi: (1) Khẳng định/câu hỏi nằm ngoài slide nguồn của bài, (2) Tóm tắt cắt mất điều kiện ngoại lệ hoặc đảo ngược quy tắc tinh vi, (3) Dùng thuật ngữ mới chưa được định nghĩa trong nguồn, và (4) Câu hỏi tương tác lộ đáp án hoặc câu chữ mơ hồ.
