# Tóm tắt mô phỏng simulate-2@20261128-125112

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| giang_vien_doi_san_xuat | 1 | 5 | 12047 | 14711 | 5.0 | 75.0 |
| ta_coach_ra_vua | 2 | 5 | 12104 | 14005 | 5.0 | 75.0 |
| ta_coach_ra_nhieu | 1 | 5 | 12275 | 15183 | 5.0 | 75.0 |

Tỉ lệ đạt dùng để tính: 24/24 (100%) — lượt run-4@20261128-123632

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-4.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (10 người) | Chi phí / tháng — cơ sở (12 người) | Chi phí / tháng — cao (15 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0247 | $0.0247 | $0.0049 | $2.33 | $2.79 | $3.49 | $0.2328 |
| gemini-4-hydrogen (vào 1.5 · ra 7.5 $/1M) | $0.1268 | $0.1268 | $0.0254 | $11.92 | $14.31 | $17.88 | $1.19 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (5.0) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: google/gemini-4-hydrogen. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 46/50.
