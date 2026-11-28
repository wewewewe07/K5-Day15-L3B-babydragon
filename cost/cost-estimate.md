# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Chấm ở rubric R6.
> Số **không điền tay**: `cost/personas.yaml` → `python run.py simulate` → chép bảng trong `cost/simulate-N-summary.md` vào đây.
> Lúc build dùng gói miễn phí / tài khoản nhóm, vẫn tính theo **giá gói trả phí** — đây là chi phí cho lúc đưa vào dùng thật.

## 1. Đầu vào

- **Người dùng** là người **duyệt** nội dung bài giảng (giảng viên / đội sản xuất / TA, coach), không phải học viên. **1 phiên = duyệt 1 bài ≈ 35 câu** (P1–P3: bản nháp 30–40 câu / ý). Bot v2 kiểm cả đoạn trong 1 lần gọi model → **1 lượt = 1 đoạn 7 câu, 5 lượt / phiên**.

  | Persona | Tỉ lệ | Bài / người / tháng | Lượt / bài (35 câu ÷ 7) | Nguồn |
  |---|---|---|---|---|
  | `giang_vien_doi_san_xuat` | 0.34 | 3 | 5 | `evidence/interviews/P1.md` |
  | `ta_coach_ra_vua` | 0.33 | 10 | 5 | `evidence/interviews/P2.md` |
  | `ta_coach_ra_nhieu` | 0.33 | 15 | 5 | `evidence/interviews/P3.md` |

  Tỉ lệ 3 kiểu theo mẫu phỏng vấn 1/1/1 *(tự ước tính)*.
- **Đầu vào mô phỏng:** 10 đoạn kịch bản, mỗi đoạn 7 câu ghép ngẫu nhiên (`random.Random(2026)`) từ câu `thuong` + `kho` của `eval/benchmark.csv` — nhãn `sinh_seed`, chỉ để đo token, không phải bằng chứng.
- **Số người dùng thật** 3 kịch bản: thấp 10 · cơ sở 12 · cao 15 người duyệt — `spec.md` §2 (~10–15 người đội sản xuất, giảng viên & TA / Coach) *(tự ước tính)*.
- **Giá** ≥2 mức model, từ `further-reading/model-prices.md` của repo đề (BTC xem 25/11/2026, https://ai.google.dev/gemini-api/docs/pricing), USD / 1 triệu token vào · ra:
  - `gemini-3.1-flash-lite` (Nhỏ): **0.25 · 1.50**
  - `gemini-4-hydrogen` (Lớn): **1.50 · 7.50**
  - Bot gọi 2 model này qua OpenRouter (`google/gemini-3.1-flash-lite`, `google/gemini-4-hydrogen`); giá OpenRouter trùng bảng BTC (https://openrouter.ai/api/v1/models, xem 28/11/2026).
- **Token đo đúng model được tính giá:** mỗi model một lượt mô phỏng riêng, chạy thật qua bot v2. Không dùng `gemini-2.5-flash` (lượt 1–2) vì bảng giá BTC ghi đã ngừng.
- **Tỉ lệ đạt** (lượt cùng model, bot v2, 24 câu): `gemini-3.1-flash-lite` **24/24 (100%)** — `run-3@20261128-123600` · `gemini-4-hydrogen` **24/24 (100%)** — `run-4@20261128-123632`.

## 2. Kết quả mô phỏng

### Model chính — `gemini-3.1-flash-lite`

Lượt mô phỏng: `cost/simulate-1.csv` · run ID `simulate-1@20261128-123921` · **50 phiên** · seed 42 · phiên lỗi 0/50 · tỉ lệ đạt từ `run-3`.

| Persona | Số phiên | Lượt / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| giang_vien_doi_san_xuat | 18 | 5 | 12268 | 2321 | 5.0 | 75.0 |
| ta_coach_ra_vua | 16 | 5 | 12266 | 2333 | 5.0 | 75.0 |
| ta_coach_ra_nhieu | 16 | 5 | 12244 | 2255 | 5.0 | 75.0 |

Thời gian bot chạy trung bình **14,2 giây / bài 35 câu** (cột `latency_s`).

### So sánh 2 mức model

| Model (token đo trên) | Chi phí / phiên (1 bài) | **Chi phí / task thành công** | / tháng — thấp (10 người) | / tháng — **cơ sở (12 người)** | / tháng — cao (15 người) | / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| **`gemini-3.1-flash-lite`** (đo trên chính nó · `simulate-1`) | $0.0065 | **$0.0065** | $0.60 | **$0.72** | $0.90 | $0.060 |
| `gemini-4-hydrogen` (đo trên chính nó · `simulate-2`, 4/50 phiên hợp lệ†) | $0.127† | **$0.127†** | $11.92† | **$14.31†** | $17.88† | $1.19† |

† `gemini-4-hydrogen` đo trên chính nó (`simulate-2@20261128-125112`), nhưng **chỉ 4/50 phiên hợp lệ**: 46 phiên lỗi HTTP 402 (tài khoản OpenRouter hết credit giữa chừng — bot khi đó chưa đặt `max_tokens`, OpenRouter giữ trước 65.536 token / lời gọi). 4 phiên hợp lệ: token vào ~12.100 / phiên (như flash-lite), **token ra ~14.500 / phiên (gấp ~6 lần flash-lite, do token suy nghĩ)**. n = 4 nhỏ → số hydrogen chỉ để so mức, không dùng làm số chính. Nếu tính giá hydrogen trên token của flash-lite (`simulate-1`) thì chỉ $0.0357 / bài — thấp hơn thật khoảng 3,5 lần, cho thấy phải đo token trên đúng model.

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt đo được (lượt cùng model). Tỉ lệ đạt đo được là 100% nên hai cột bằng nhau — **không phải do giả định 100%**. Xem độ nhạy ở mục 4 cho tỉ lệ thấp hơn.

## 3. So với impact

- **Impact / người / tháng** (`spec.md` §2): 1.575 phút công duyệt / tháng ÷ 12 người ≈ **131 phút (~2,2 giờ) dò nguồn thủ công / người / tháng** *(chia đều — tự ước tính)*; P1–P3 tự kể 15–60 phút / bài.
- **Chi phí / người / tháng** (cơ sở, `gemini-3.1-flash-lite`): **$0.06** — cả đội 12 người **$0.72 / tháng**.
- **Kết luận một dòng — đáng làm:** chi phí model gần như bằng 0 (dưới 1 USD / tháng cho cả đội, ~0,7 cent / bài) so với ~26 giờ công duyệt / tháng; chỉ cần bot rút ngắn **1 phút** mỗi bài là đã lời. Thứ quyết định đáng làm hay không là **bot có giúp giảng viên duyệt nhanh hơn mà không lọt lỗi hay không** — chưa đo được với người dùng thật (`eval/report.md` §4), không phải tiền model.
- **Chọn model:** `gemini-4-hydrogen` đắt hơn khoảng 20 lần nhưng đạt **bằng** `gemini-3.1-flash-lite` trên cả bộ chính thức (24/24) và bộ chịu tải (27/27), lại chậm hơn → chọn **`gemini-3.1-flash-lite`**.

## 4. Độ nhạy & chi phí ngoài model *(muốn sâu hơn)*

| Cần gạt | Chi phí / task thành công (`gemini-3.1-flash-lite`) | Ghi chú |
|---|---:|---|
| Cơ sở (tỉ lệ đạt 100%, `run-3`) | $0.0065 | |
| Tỉ lệ đạt = ngưỡng chuẩn 80% (§7) | $0.0081 | ÷ 0,80 |
| Tỉ lệ đạt = bot v1 trên bộ chịu tải (21/26 = 80,8%) | $0.0080 | kịch bản bot kém hơn trên đầu vào khó |
| Bài dài gấp đôi (70 câu, 10 lượt) | ~$0.013 | token tăng gần tuyến tính theo số lượt |
| Quy mô cả khoá cao gấp 3 (45 người duyệt) | — | ~$2.7 / tháng (cơ sở × 45 / 12) |

- **Chi phí ngoài model (chưa tính):** hosting một tiến trình Python nhỏ · giờ công giảng viên vẫn phải đọc bảng kiểm duyệt và quyết định — bot không thay giảng viên mà rút ngắn việc dò nguồn.
- **Giới hạn:** đoạn kịch bản ghép từ câu benchmark (ngắn, đã gắn tiền tố bài), kịch bản thật có thể dài hơn và cần kho nguồn lớn hơn 12 đoạn → token vào / lượt có thể tăng; dù tăng 10 lần chi phí cả đội vẫn dưới $10 / tháng.
