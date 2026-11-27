# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.
> **Ghi chú nhóm `babydragon`:** Chuẩn bị sẵn giả thuyết cho 3 lát cắt dự bị **A5**, **D2**, **E1** trước khi tiến hành phỏng vấn và khảo sát tại lớp L3B.

- Ngày giờ viết: 27/11/2026 14:15

---

## 🅰️ Giả thuyết Phương án A5 (Track A — Vận hành đào tạo: Lịch, phòng, phân công Lab Coach)

- **Người dùng chính (một vai cụ thể):** Key Coach / Day Lead và Lab Coach của lớp L3 khoá AI20K.
- **Mình nghĩ:** Key Coach gặp khó khi đối chiếu phòng học chốt sát giờ và yêu cầu đổi ca của Lab Coach trước buổi lab vì thông tin nằm rải rác ở 2 file bảng tính khác nhau (`teaching-schedule` và `lab-coach-schedule`, mỗi ô ghi chữ tự do nhiều dòng) cùng tin nhắn Zalo, hậu quả là mất 30–60 phút dò tay mỗi buổi và dễ xảy ra sót lỗi trùng ca hoặc báo nhầm phòng.
- **Có thể còn cách giải thích khác:** Key Coach đã quen nhìn bằng mắt và chỉ có rất ít phòng bị đổi sát giờ nên việc đối chiếu thủ công chỉ mất dưới 5 phút, không phải chỗ đau lớn.
- **Mình đúng nếu thấy:** ≥2/3 Key Coach / Lab Coach được phỏng vấn kể được ít nhất 1 lần trong 1 tháng qua bị vướng/mất >15 phút vì lịch phòng chốt muộn hoặc lệch thông tin đổi ca giữa các bảng.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [ ] đào data · [x] phỏng vấn ≥3 · [ ] khảo sát ≥20 — **nguồn chính:** Phỏng vấn ≥3 Key Coach / Lab Coach tại lớp L3B · **nguồn để kiểm lại:** Phân tích cấu trúc thực tế & lịch sử chỉnh sửa trong bộ dữ liệu mẫu `data/training-ops/`.

---

## 🅳 Giả thuyết Phương án D2 (Track D — Đặt đơn đồ ăn nhóm có ràng buộc ăn uống & ngân sách)

- **Người dùng chính (một vai cụ thể):** Học viên / nhân viên văn phòng thường xuyên đứng ra đặt đồ ăn trưa hoặc tối hộ cả nhóm 4–8 người trên app giao đồ ăn (ShopeeFood, GrabFood, BeFood).
- **Mình nghĩ:** Người đặt hộ gặp khó khi phải chọn combo/món lẻ từ menu một quán sao cho vừa khớp ngân sách bình quân (đã tính phí ship/voucher) vừa không vi phạm các yêu cầu riêng (ăn chay, dị ứng hải sản/đậu phộng/sữa), hậu quả là mất 15–30 phút trao đổi qua lại và cộng nhẩm, hoặc đặt nhầm món người trong nhóm không ăn được / lố ngân sách.
- **Có thể còn cách giải thích khác:** Các nhóm thường chỉ đặt 1 món giống hệt nhau hoặc dùng tính năng "Đặt đơn nhóm" (Group Order) có sẵn của app nên người đặt hộ không phải tự chọn hay tự kiểm tra ràng buộc.
- **Mình đúng nếu thấy:** ≥2/3 người phỏng vấn (≥2/3) và ≥50% người trả lời khảo sát (≥10/20 người) xác nhận trong 1 tháng qua phải tự gom yêu cầu ăn uống/ngân sách của nhóm, mất ≥15 phút mỗi lần hoặc từng tính lệch phí ship / nhầm yêu cầu ăn uống.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [x] đào data · [x] phỏng vấn ≥3 · [x] khảo sát ≥20 — **nguồn chính:** Khảo sát ≥20 học viên lớp L3B + Phỏng vấn ≥3 người đặt đơn nhóm · **nguồn để kiểm lại:** Đào review công khai liên quan đến đặt đơn nhóm / ghi chú thành phần món ăn trên Google Play & App Store.

---

## 🅴 Giả thuyết Phương án E1 (Track E — Giải thích chi tiêu từ sao kê lộn xộn)

- **Người dùng chính (một vai cụ thể):** Nhân viên văn phòng trẻ / học viên đi làm sử dụng ví điện tử (MoMo, ZaloPay) và app ngân hàng cho >50 giao dịch/tháng.
- **Mình nghĩ:** Người dùng gặp khó khi muốn rà soát "tháng này tiền đi đâu nhiều nhất" hoặc "tại sao chi tiêu tháng này tăng" vì sao kê hiển thị hàng loạt mã merchant viết tắt khó hiểu (`XEMAU*BIKE`, `VNPay*...`) và giao dịch chuyển khoản không ghi rõ nội dung, trong khi biểu đồ có sẵn của app gán nhãn sai hàng loạt vào mục "Chuyển tiền / Khác", hậu quả là họ mất 20–30 phút tự tra soát tay hoặc bỏ cuộc không kiểm soát được chi tiêu.
- **Có thể còn cách giải thích khác:** Thống kê tự động có sẵn trên app ngân hàng/ví điện tử đã phân loại đủ chính xác, người dùng không có nhu cầu hỏi sâu hơn bằng ngôn ngữ tự nhiên.
- **Mình đúng nếu thấy:** ≥2/3 người được phỏng vấn và ≥60% người khảo sát (≥12/20 người) cho biết trong 1 tháng qua khi mở sao kê/thống kê chi tiêu đã gặp các giao dịch không nhớ nổi là chi cho việc gì hoặc bị app gom nhầm vào mục "Khác/Chuyển khoản", phải tự cộng lại hoặc bỏ cuộc.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [x] đào data · [x] phỏng vấn ≥3 · [x] khảo sát ≥20 — **nguồn chính:** Khảo sát ≥20 học viên lớp L3B + Phỏng vấn ≥3 người dùng ví/ngân hàng · **nguồn để kiểm lại:** Đào 100 review công khai của app ví điện tử / ngân hàng trên Google Play & App Store về tính năng quản lý chi tiêu / sao kê.
