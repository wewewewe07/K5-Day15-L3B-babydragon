# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Ôn lại: ngày 13, ngày 1, ngày 14 · lab ngày 13, lab ngày 14. Chấm ở rubric R6.
> Số **không điền tay**: điền `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu người duyệt kịch bản bài giảng. 1 phiên = duyệt 1 kịch bản, 1 lượt = 1 đoạn ~6–8 câu.

  | Persona | Tỉ lệ | Kịch bản / người / tháng | Lượt / phiên |
  |---|---|---|---|
  | `giang_vien_soan_bai_moi` | 0.5 | 4 | 6 |
  | `doi_san_xuat_duyet_dinh_ky` | 0.3 | 3 | 4 |
  | `phu_trach_soat_bai_cu` | 0.2 | 2 | 2 |

  Nguồn: "soạn 1 bài / tuần (nhiều lượt)" và "soát bài cũ (ít lượt)" lấy từ đề track A mục A3 (`tracks/track-a-edtech.md` của repo đề). Kịch bản 30–50 câu lấy từ `spec.md` §1. Các số còn lại *(tự ước tính)*, sẽ cập nhật sau phỏng vấn.
- **Số người dùng thật** 3 kịch bản: thấp 10 · cơ sở 12 · cao 15 người duyệt. Nguồn: `spec.md` §2 (~10–15 người đội sản xuất & giảng viên) *(tự ước tính)*. Kiểm chéo: cơ sở ra ~40 kịch bản / tháng, khớp 30–45 kịch bản / tháng ở §2.
- **Giá** ≥2 mức model (từ `further-reading/model-prices.md` của repo đề, BTC xem 25/11/2026, link https://platform.claude.com/docs/en/about-claude/pricing): Claude Haiku 5.5 (Nhỏ) 0.10 / 0.50 USD mỗi 1M token vào / ra · Claude Sonnet 5.5 (Lớn) 2.00 / 10.00
- **Giới hạn:** mỗi lượt mô phỏng lấy đầu vào từ `eval/benchmark.csv`, nên token / lượt của persona "soát bài cũ" (thực tế token rất lớn) có thể bị tính thấp.
- **Tỉ lệ đạt** dùng để tính: __/__ (__%) — lượt `run-__` (lượt 2)
- Đo token trên model __, tính giá model __ và __

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
