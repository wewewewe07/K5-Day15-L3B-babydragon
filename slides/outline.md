# Dàn Slide & Kịch Bản Thuyết Trình (Pitch Script) — Nhóm babydragon (L3B · Track A3)

> Làm ở guide bước 5.1 & 5.3. Luật: **không có bằng chứng thì không có slide** — mỗi trang ≥1 con số / trích dẫn có nguồn / kết quả đo.
> File PDF chính thức: [demo-slides.pdf](../demo-slides.pdf) ở thư mục gốc repo · Video dự phòng: https://youtu.be/6wmDIAIMmrM · Giao diện Web Demo: `python ui/server.py`

## 1. Bảng ánh xạ 8 trang Slide → Nguồn dữ liệu & Phân công người nói

| # | Trang Slide | Có gì | Số lấy từ | Người nói | Xong |
|---|---|---|---|---|---|
| 0 | **Trang Bìa** | Tên đề tài Track A3 · Lát cắt · 4 thành viên nhóm `babydragon` | `TEAMS.md`, `canvas.md` | **Bùi Đình Quý Anh** | ☑ |
| 1 | **1 · Người dùng & pain** | 3/3 người dạy (15–60 phút/bài) · P3 rà 15 bài/tháng chỉ đọc lướt · 12/21 học viên gặp câu hỏi thiếu ngữ cảnh + 2 trích dẫn nguyên văn | `evidence/summary.md`, `P1.md`–`P3.md`, `results.csv` | **Bùi Đình Quý Anh** | ☑ |
| 2 | **2 · Vì sao chọn bài này** | Bảng so sánh Impact A3 (1.575 phút công duyệt + 15.666 phút học viên) vs A1 vs A5 | `spec.md` §2 | **Bùi Đình Quý Anh** | ☑ |
| 3 | **3 · Giải pháp** | Lát cắt 1 câu · Sơ đồ Workflow cố định 5 bước · 5 nhãn đầu ra · Mức tự động 1 (AI gợi ý, người quyết, HAX G10) | `spec.md` §4, `codebase/agent.py` | **Nguyễn Thanh Tùng** *(Lead)* | ☑ |
| 4 | **4 · Demo live** | Chạy trực tiếp trên Web UI (`python ui/server.py`) hoặc CLI (`python run.py`): 1 câu thường (`B01`) + 1 câu khó/tấn công nguỵ tạo mã nguồn (`B15`) + kịch bản nhiều Slide (`/demo`) | `eval/benchmark.csv`, `eval/run-3.csv` | **Nguyễn Thanh Tùng** *(Lead)* | ☑ |
| 5 | **5 · Đánh giá thế nào** | 24 câu thử (15/24 từ người dùng/data thật) · 3 metric (chấm chéo 5/5) · Lượt 1→4 (24/24) · Bộ chịu tải 27 câu khó (Bot v1: 21/26 → Bot v2: 26/26 & 27/27) | `eval/README.md`, `eval/report.md` | **Giang Thái Sơn** | ☑ |
| 6 | **6 · Chi phí khi dùng thật** | 3 persona (3 · 10 · 15 bài/tháng) · 50 phiên chạy thật · `$0.0065 / bài đạt` (`gemini-3.1-flash-lite`) · `$0.72 / tháng` (cơ sở 12 người) vs `gemini-4-hydrogen` (`$0.127/bài`) | `cost/personas.yaml`, `cost/cost-estimate.md` | **Trịnh Ngọc Ninh** | ☑ |
| 7 | **7 · Kết luận** | Quyết định **Iterate → Pilot** dẫn số từ Trang 1, 5, 6 | `spec.md` §7–§8, `eval/report.md` | **Trịnh Ngọc Ninh** | ☑ |
| 8 | **8 · Nếu có thêm 1 tuần** | Tập held-out 30–40 câu kịch bản thật · Ca 2 nguồn mâu thuẫn · Pilot với 2–3 giảng viên thật & cải tiến UX từ `U1`, `U2` | `eval/report.md` §4, `validation/log.md` | **Trịnh Ngọc Ninh** | ☑ |

---

## 2. Kịch bản lời thoại chi tiết (Tổng thời lượng: ~4 phút 30 giây)

### 🎤 PHẦN 1: Bùi Đình Quý Anh (Trang Bìa + Trang 1 + Trang 2 — ~1 phút 15 giây)

**[Trang Bìa]**
> "Xin chào Ban giám khảo và các bạn, chúng mình là nhóm **babydragon** lớp **L3B**. Hôm nay nhóm trình bày giải pháp cho **Track A3**: **Kiểm duyệt kịch bản bài giảng và câu hỏi tương tác do AI sinh, từng câu trỏ về đoạn nguồn chuẩn của khoá học**."

**[Trang 1 · Người dùng & Pain]**
> "Để chứng minh nỗi đau là có thật, nhóm đã thu thập đủ **3 nguồn bằng chứng**: phỏng vấn sâu **3 người trực tiếp làm nội dung và rà bài (`P1`–`P3`)**, khảo sát phân nhánh **24 người (3 Giảng viên/Coach và 21 Học viên L3)**, và đào **107.709 dòng log `data/preclass/`**.
> - Từ phía **Người dạy**: Cả **3/3 người** xác nhận bản nháp AI sinh 30–40 câu rất trôi chảy nhưng hay cài cắm kiến thức ngoài bài hoặc sai điều kiện tinh vi — trích nguyên văn là *'sinh sai nội dung'*, *'nội dung quá bịp'*. Giảng viên `P1` phải mở song song 2 cửa sổ đọc dò bằng mắt mất **30–60 phút mỗi bài**; còn Coach `P3` vì phải rà tới **15 bài/tháng** nên không đủ thời gian tra nguồn, đành *'chỉ đọc lướt theo trí nhớ chuyên môn'*.
> - Chính vì chỉ đọc lướt nên lỗi lọt xuống **Học viên**: Trong khảo sát, **12/21 học viên (57,1%)** gặp câu hỏi hỏi ý chưa được giảng trong đoạn bài trước đó (như hỏi về *Google PAIR* hay *Lost in the Middle* khi slide bài đó không có), và **15/21 bạn (71,4%)** mất từ **5 đến trên 30 phút** mỗi lần phải tự tua lại video hoặc dò lại bài đọc gốc."

**[Trang 2 · Vì sao chọn bài này]**
> "Khi so sánh 3 hướng trên bảng Impact: Hướng A1 (Tutor dưới video) chỉ chữa cháy ở ngọn sau khi học viên đã bị kẹt; Hướng A5 (Lịch phòng) có tần suất thấp hơn. Nhóm chọn **A3** vì nó **chặn lỗi ngay từ gốc trước khi xuất bản cho hơn 700 học viên**. Với quy mô **35 kịch bản/tháng × 45 phút dò nguồn**, A3 tác động trực tiếp tới **1.575 phút (~26 giờ) công chuyên gia** và hơn **15.600 phút học viên phải tự dò lại bài mỗi tháng**."

---

### 🎤 PHẦN 2: Nguyễn Thanh Tùng — Đội trưởng (Trang 3 + Trang 4 Demo Live — ~1 phút 30 giây)

**[Trang 3 · Giải pháp]**
> "Lát cắt của nhóm là: **Một giảng viên đưa đoạn kịch bản hoặc câu hỏi tương tác do AI sinh vào → Hệ thống đối chiếu với kho tài liệu nguồn chính thức của khoá để quyết định gắn 1 trong 5 nhãn (`KHOP_NGUON`, `SAI_MAU_THUAN`, `LOI_CAU_HOI`, `THIEU_NGUON`, `TU_CHOI`) kèm mã đoạn `[SRC-...]` và gợi ý câu sửa → Giảng viên duyệt chấp nhận hoặc sửa trước khi xuất bản.**
> - Nhóm chọn hình dạng **Workflow cố định 5 bước** thay vì Agent tự do vì mọi câu khẳng định trong bài giảng đều bắt buộc phải đi qua bước kiểm tra mã nguồn bằng code, không được phép nhảy bước:
>   1. Bước 1: Code `split_claims` tách đoạn kịch bản thành từng câu khẳng định hoặc khối câu hỏi Quiz.
>   2. Bước 2: Công cụ `search_sources` và `get_segment` truy xuất đoạn nguồn theo từng câu.
>   3. Bước 3: Code `check_claim` tiền kiểm phát hiện mã nguồn giả, câu hỏi lộ đáp án và prompt injection.
>   4. Bước 4: Model đối chiếu ngữ nghĩa từng câu với đoạn nguồn và đề xuất câu viết lại (`Sửa thành "..."`).
>   5. Bước 5: Code Guardrail hậu kiểm chặn 100% mã nguồn không tồn tại, tự động lấy nhãn nghiêm trọng nhất của cả đoạn và đẩy vào `submit_for_review` chờ giảng viên duyệt.
> - Về mức tự động: **AI chỉ gợi ý, giảng viên quyết định — cấm tự xuất bản**. Khi thông tin không có trong nguồn khoá học, áp dụng nguyên tắc **HAX G10**: thu hẹp phạm vi, bắt buộc gắn `THIEU_NGUON` để giảng viên quyết."

**[Trang 4 · Demo Live]** *(Mở giao diện Web `python ui/server.py` hoặc CLI `python run.py`)*
> "Nhóm đã xây dựng cả giao diện dòng lệnh (`python run.py` với chế độ `/multi` và `/demo`) lẫn giao diện Web trực quan (`python ui/server.py`) gọi cùng hàm `answer()` với model thật `google/gemini-3.1-flash-lite`:
> 1. **Ca thứ nhất (Đoạn kịch bản nhiều Slide + Lời giảng trộn Đúng & Sai):** Hệ thống tách từng câu, chỉ rõ câu nào `KHOP_NGUON`, câu nào `THIEU_NGUON`, câu nào `SAI_MAU_THUAN`, chốt nhãn tổng theo câu nặng nhất và viết sẵn câu gợi ý sửa cho giảng viên.
> 2. **Ca thứ hai (Ca tấn công nguỵ tạo nguồn `B15`):** Câu này viết sai quy tắc Mom Test nhưng **cố tình gắn sẵn mã nguồn thật `[SRC-D02-M1-01]` ở cuối câu để đánh lừa bộ kiểm duyệt**. Hệ thống dùng `get_segment` đọc nội dung thật của `SRC-D02-M1-01` lên đối chiếu, bắt lỗi ngay **`SAI_MAU_THUAN [SRC-D02-M1-01]`** và hiển thị nguyên văn đoạn nguồn gốc ngay bên dưới để giảng viên kiểm tra trong 3 giây."

---

### 🎤 PHẦN 3: Giang Thái Sơn (Trang 5 · Đánh giá thế nào — ~1 phút)

**[Trang 5 · Đánh giá thế nào]**
> "Về đánh giá, nhóm xây dựng bộ câu thử chính thức `eval/benchmark.csv` gồm **24 câu** (9 `thuong`, 11 `kho`, 4 `tu_choi`), với **15/24 câu (62,5%)** lấy từ phản hồi người dùng thật và dữ liệu `preclass`. Ba metric trong `metric_spec.yaml` đã được 2 thành viên chấm chéo độc lập đạt độ khớp **5/5**.
> - Ở **Lượt 1 (`run-1`)**, bot v1 đạt **24/24 (100%)** trên bộ chính thức. Nhưng vì bộ đầu mỗi câu chỉ có 1 khẳng định đơn lẻ nên nhóm thiết kế thêm **bộ chịu tải 27 câu khó (`tests/stress_cases.csv`)** gồm kịch bản nhiều câu, diễn đạt bằng tiếng Anh, và gắn mã giả vào câu đúng.
> - Khi đưa vào bộ chịu tải, **bot v1 lộ ra ngay 5 câu trượt (chỉ đạt 21/26 = 80,8%)**. Lỗi đau nhất với giảng viên là câu **`S12`**: kịch bản có câu đầu đúng ghép với câu sau bịa số liệu *'Gartner 87%'*, bot v1 chỉ xét câu đầu rồi cho qua cả đoạn là `KHOP_NGUON`!
> - Nhóm thực hiện **1 lần cải tiến lên Bot v2**: bổ sung bộ tách câu `split_claims`, tra nguồn theo từng câu, bổ sung từ khoá tiếng Anh và dùng code lấy nhãn nặng nhất. Kết quả sau cải tiến: Bộ chịu tải tăng từ **21/26 lên 26/26 (100%)**, và khi chạy Lượt 3, Lượt 4 trên 2 model trong bảng giá BTC (`gemini-3.1-flash-lite` và `gemini-4-hydrogen`) đều đạt tuyệt đối **24/24 trên bộ chính thức và 27/27 trên bộ chịu tải**."

---

### 🎤 PHẦN 4: Trịnh Ngọc Ninh (Trang 6 + Trang 7 + Trang 8 — ~1 phút)

**[Trang 6 · Chi phí khi dùng thật]**
> "Để tính chi phí khi đưa vào vận hành thật cho khoá học: 1 bài giảng trung bình có **35 câu**, bot v2 kiểm 7 câu mỗi lượt nên **1 phiên duyệt 1 bài = 5 lượt gọi model**. Nhóm khai báo 3 persona từ đúng số liệu phỏng vấn `P1`, `P2`, `P3` (duyệt 3, 10 và 15 bài/tháng) và chạy mô phỏng thật **50 phiên (`simulate-1`)**.
> - Với model chính **`gemini-3.1-flash-lite`**, **Chi phí trên mỗi bài duyệt thành công là `$0.0065` (~160 đồng/bài)**, thời gian xử lý trung bình **14,2 giây/bài 35 câu**.
> - Phóng lên quy mô thật của đội ngũ duyệt bài toàn khoá ở 3 kịch bản (Thấp 10 người · Cơ sở 12 người · Cao 15 người), tổng chi phí chỉ là **`$0.60` · `$0.72` · `$0.90 / tháng`** (tức **`$0.06 / người / tháng`**) — rẻ hơn khoảng **20 lần** so với `gemini-4-hydrogen` (`$0.127/bài`, `$14.31/tháng`) mà chất lượng ngang nhau. So với **~131 phút** dò nguồn thủ công mỗi người mỗi tháng, chi phí model hoàn toàn không phải rào cản."

**[Trang 7 & Trang 8 · Kết luận & Nếu có thêm 1 tuần]**
> "Từ các con số trên, quyết định của nhóm ở Trang 7 là **ITERATE → PILOT (Chưa Go đại trà ngay)**:
> - Dù chất lượng trên benchmark đạt chuẩn và chi phí chỉ `$0.72/tháng`, mọi con số hiện tại mới đo trên kho nguồn rút gọn 12 đoạn và bộ câu thử do nhóm thiết kế.
> - **Nếu có thêm 1 tuần (Trang 8)**, nhóm sẽ làm 3 việc: (1) Lấy **20 kịch bản bài giảng thật của khoá làm tập giữ riêng (held-out)** để giảng viên chấm mù; (2) Bổ sung kịch bản xử lý **2 nguồn tài liệu mâu thuẫn nhau hoặc tài liệu cũ/mới**; và (3) Tiếp tục hoàn thiện trải nghiệm từ 2 buổi người dùng thử (`U1`, `U2` trong `validation/log.md`) và **pilot trên 1 bài sắp xuất bản với 2–3 giảng viên** để đo thời gian duyệt trước và sau. Xin cảm ơn Ban giám khảo!"
