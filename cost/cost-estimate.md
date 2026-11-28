# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu người duyệt nội dung bài giảng. 1 phiên = duyệt 1 bài, 1 lượt = 1 câu khẳng định (`agent.py` kiểm từng câu, mỗi câu 1 lần gọi model).

  | Persona | Tỉ lệ | Bài / người / tháng | Câu / bài | Nguồn |
  |---|---|---|---|---|
  | `giang_vien_doi_san_xuat` | 0.34 | 3 | 35 | P1 |
  | `ta_coach_ra_vua` | 0.33 | 10 | 35 | P2 |
  | `ta_coach_ra_nhieu` | 0.33 | 15 | 35 | P3 |

  Số bài / tháng lấy từ phỏng vấn `evidence/interviews/P1.md`–`P3.md`. 35 câu / bài lấy giữa khoảng 30–40 câu / ý của bản nháp (câu 3 phỏng vấn, `spec.md` §1). Tỉ lệ 3 kiểu theo mẫu phỏng vấn 1/1/1 *(tự ước tính)*.
- **Số người dùng thật** 3 kịch bản: thấp 10 · cơ sở 12 · cao 15 người duyệt. Nguồn: `spec.md` §2 (~10–15 người đội sản xuất, giảng viên & TA/Coach) *(tự ước tính)*.
- **Giá** ≥2 mức model (từ `further-reading/model-prices.md` của repo đề, BTC xem 25/11/2026, link https://ai.google.dev/gemini-api/docs/pricing): `gemini-3.1-flash-lite` (Nhỏ) 0.25 / 1.50 USD mỗi 1M token vào / ra · `gemini-4-hydrogen` (Lớn) 1.50 / 7.50
- **Tỉ lệ đạt** dùng để tính: __/__ (__%) — lượt `run-__` (lượt 2)
- Đo token trên model `google/gemini-2.5-flash` (OpenRouter, model của lượt eval), tính giá model `gemini-3.1-flash-lite` và `gemini-4-hydrogen`. Lý do: bảng giá BTC ghi `gemini-2.5-flash` đã ngừng, không dùng trong bảng chi phí.
- **Giới hạn:** mỗi lượt mô phỏng lấy ngẫu nhiên 1 câu trong `eval/benchmark.csv`; câu trong kịch bản thật có thể dài hơn nên token / lượt có thể bị tính thấp.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · __ phiên · seed __

*(dán bảng từ `cost/simulate-N-summary.md`)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp | / tháng — cơ sở | / tháng — cao | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt — **không coi như đạt 100%**.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): __
- Chi phí / người / tháng (cơ sở, model __): __
- **Kết luận một dòng — đáng làm không:** __

## 4. *(Muốn sâu hơn, không bắt buộc)*

- Bảng độ nhạy: model rẻ hơn · cache · cắt ngữ cảnh · giới hạn bước — mỗi cần gạt đổi chi phí bao nhiêu
- Chi phí ngoài model: hosting, lưu trữ, giờ công người duyệt
- Quy mô nào thì bài toán còn đáng làm
