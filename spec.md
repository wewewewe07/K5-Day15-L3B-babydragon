# AI SPEC — Duyệt kịch bản bài giảng: đánh dấu câu sai / thiếu nguồn · Nhóm babydragon · Lớp L3B · Phòng __ · Zone __

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: **A3 · Sản xuất bài giảng bằng AI** — rà soát kịch bản bài giảng pre-class do AI soạn nháp, đánh dấu câu sai / thiếu nguồn để giảng viên duyệt.
Data BTC cấp đã dùng (nếu có — không commit nguyên file): `data/preclass/` (dự kiến, chỉ để đào tín hiệu phụ; repo chỉ giữ số đã tổng hợp).

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại *(giả định ban đầu — sẽ kiểm qua phỏng vấn đội sản xuất bài giảng)*:
  1. Giảng viên / đội sản xuất dùng công cụ AI soạn nháp kịch bản lời giảng cho một video pre-class từ slide và dàn ý.
  2. Người duyệt đọc từng câu của bản nháp, tự mở slide / tài liệu gốc để kiểm câu nào đúng, câu nào lấy từ đâu.
  3. Sửa trực tiếp trên tài liệu, ghi chú bằng comment hoặc nhắn trao đổi trong nhóm.
  4. Quay / dựng video và đăng lên trang pre-class; lỗi phát hiện sau đó thường đến từ câu hỏi của học viên.
- Công cụ / AI đang được dùng cho việc này: chatbot AI để soạn nháp, Google Docs / Slides để duyệt — **chưa kiểm**, sẽ hỏi trong phỏng vấn.

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính (một vai cụ thể): giảng viên / thành viên đội sản xuất bài giảng online của khoá, người duyệt kịch bản cho một video pre-class.
- Việc họ cố làm xong (không có chữ AI): duyệt kịch bản lời giảng của một video pre-class cho đúng kiến thức và có nguồn, trước khi quay hoặc đăng.
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: đọc và dò tay với slide / tài liệu gốc; hỏng vì bản nháp không trỏ câu nào về nguồn nào, lỗi tinh vi dễ lọt; chưa bỏ vì chưa có cách nào kiểm nhanh mà vẫn để người duyệt giữ quyền quyết *(giả định, chờ phỏng vấn)*.
- Pain (KHÔNG chữ AI): giảng viên duyệt bản nháp kịch bản ~40 câu cho một video pre-class phải tự dò từng câu với slide, tài liệu gốc vì bản nháp không trỏ về nguồn, nên mất nhiều thời gian mỗi video và vẫn có thể lọt câu sai lên bài giảng cho hàng trăm học viên.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): *chưa có — CP1 chỉ có giả thuyết ở `evidence/hypothesis.md`; phỏng vấn ≥3 người tối 27/11.*

## §2. Impact & quyết định chọn *(guide 1.3)*

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| **A3 · Duyệt kịch bản bài giảng do AI soạn nháp** | __ giảng viên / người làm nội dung *(chờ phỏng vấn)* | __ video / tháng *(chờ phỏng vấn)* | ≥30 phút dò nguồn / video *(giả thuyết)* + rủi ro lọt lỗi tới ~700 học viên L3 *(quy mô từ track A)* | __ *(điền sau phỏng vấn)* | Kịp: lát cắt chỉ làm một quyết định (đánh dấu từng câu) | **Chọn** |
| A1 · Trợ giảng dưới video trả lời kèm mã đoạn | 145/436 học viên có hoạt động từng hỏi trợ giảng *(data preclass, đếm nhanh 27/11)* | 1.260 lượt chat / 05–25/11 *(data preclass)* | thời gian tự tua lại video khi câu trả lời không có mốc trích *(tự ước tính)* | __ | Kịp | Giữ so sánh |
| A5 · Đối chiếu lịch phòng & ca lab coach | ~vài key coach *(tự ước tính)* | mỗi tối trước buổi lab *(track A)* | 30–60 phút dò tay *(tự ước tính)* | __ | Vừa — đọc xlsx giả lập tốn thời gian | Loại |

- **Impact / tháng** của hướng chọn = __ người × __ video × __ phút = __ — nguồn từng thừa số: phỏng vấn (chưa có) · *(tự ước tính cho tới khi có số)*
- Hướng ĐÃ LOẠI + vì sao (giữ lại, đừng xoá): A5 — data training-ops là giả lập, không phải bằng chứng, file khó đọc; trước đó nhóm cũng cân nhắc D2 (đặt đồ ăn nhóm) và E1 (sao kê) nhưng chọn ở lại Track A vì gần với người dùng trong khoá.
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8): soạn mới 1 bài / tuần (nhiều lượt, token lớn) · soát lại bài cũ (ít lượt, token rất lớn) *(theo gợi ý persona A3 của track; số thật lấy từ phỏng vấn)*.

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả):
- Không làm (≥3 điều):
- **Sơ đồ** (ảnh / Mermaid / draw.io): [chèn ở đây]
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do (sai thì ai chịu gì, sửa đắt hay rẻ):
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì):
- **Chỗ người duyệt** (việc AI không được tự làm):
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): **Nguyễn Thanh Tùng** (Lead, kiến trúc & luồng agent) · **Giang Thái Sơn** (bộ kịch bản mẫu + tài liệu nguồn, `check_claim`) · **Bùi Quý Anh** (phỏng vấn, bộ câu thử) · **Trịnh Ngọc Ninh** (chi phí, slide).
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |
