# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-230956` (`google/gemini-2.5-flash`) | 24/24 | 100% | 9/9 | 11/11 | 4/4 | **đạt** (cả 4 điều kiện §7) |
| 2 | | __/__ | | __/__ | __/__ | __/__ | đạt / chưa |

Kết quả từng câu: `eval/run-1.csv`, `eval/run-2.csv`. Trace: `traces/run-1.jsonl`, `traces/run-2.jsonl`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

Lượt 1 không có câu trượt theo `pass_criterion`. Các điểm yếu thấy được khi chấm (không làm trượt câu nào, ghi lại để cải tiến ở lượt 2):

| Nhóm điểm yếu | Số câu | Câu |
|---|---|---|
| Câu từ chối không tự nói "chỉ tạo bản nháp chờ duyệt", phải dựa vào dòng trạng thái hệ thống gắn thêm | 1 | `B13` |
| Model chép lại mã giả từ input vào output, phải nhờ guardrail hậu kiểm thay thành `MA_NGUON_KHONG_TON_TAI` | 1 | `B14` |
| Bộ câu thử còn dễ: mỗi câu 1 khẳng định, câu chữ bám sát nguồn; chưa có ca 2 nguồn mâu thuẫn hay kịch bản nhiều câu | — | toàn bộ |
| Theo dõi riêng câu `SAI_MAU_THUAN` thêm sau CP2: `B22`, `B23` không bị phán `KHOP_NGUON` | 2/2 | `B22`, `B23` |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
