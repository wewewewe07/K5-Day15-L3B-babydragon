# Tóm tắt mô phỏng simulate-1@20261128-123921

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| giang_vien_doi_san_xuat | 18 | 5 | 12268 | 2321 | 5.0 | 75.0 |
| ta_coach_ra_vua | 16 | 5 | 12266 | 2333 | 5.0 | 75.0 |
| ta_coach_ra_nhieu | 16 | 5 | 12244 | 2255 | 5.0 | 75.0 |

Tỉ lệ đạt dùng để tính: 24/24 (100%) — lượt run-3@20261128-123600

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (10 người) | Chi phí / tháng — cơ sở (12 người) | Chi phí / tháng — cao (15 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0065 | $0.0065 | $0.0013 | $0.6024 | $0.7229 | $0.9036 | $0.0602 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.0357 | $0.0357 | $0.0071 | $3.30 | $3.96 | $4.94 | $0.3296 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (5.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: google/gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
