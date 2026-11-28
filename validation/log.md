# Người dùng thử CP4

## Trạng thái bonus

**0/2 buổi dùng thử với người ngoài nhóm đã được ghi nhận.** Có một lượt chạy thử nội bộ bằng Codex để chuẩn bị. [Rubric bonus](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/03-rubric.md#bonus)

## Chạy thử nội bộ · 28/11/2026

Codex gửi đầu vào qua CLI `python run.py` trên bản `2af3fdc`, ở chế độ `fake` (0 token). Các dòng dưới đây ghi hành vi của ứng dụng trong lượt chạy.

| Việc thử | Quan sát | Mức ảnh hưởng |
|---|---|---|
| Rà một câu đúng trong kịch bản (B01) | CLI in `KHOP_NGUON [SRC-D02-M2-01]` và trạng thái `PENDING_LECTURER_REVIEW`. Mã nguồn nằm ngay cạnh nhãn. | Thấp |
| Kiểm tra trạng thái khi yêu cầu xuất bản (B13) | CLI in `TU_CHOI` và dòng “Chờ giảng viên duyệt, tự động xuất bản: False”. | Thấp |
| Rà một đoạn hai câu theo đúng cách xuống dòng của bản nháp | Khi hai câu nằm cùng một dòng, CLI trả một kết quả và ghi 1 lần gọi model. Khi đặt mỗi câu trên một dòng, CLI trả hai kết quả riêng, mỗi kết quả ghi 1 lần gọi model. Người duyệt phải đọc từng kết quả để tổng hợp lại cả đoạn. | Vừa |

Bản chạy thật lưu trong [eval/run-3.csv](../eval/run-3.csv) có B01 trả `KHOP_NGUON [SRC-D02-M2-01]` và B15 trả `SAI_MAU_THUAN [SRC-D02-M1-01]`. Lượt nội bộ hôm nay chỉ kiểm tra cách nhập và trạng thái trong CLI.

**Điều chỉnh đã làm:** README hướng dẫn thay chỗ xuống dòng bằng dấu cách, giữ dấu kết câu, rồi nhấn Enter một lần khi muốn kiểm cả đoạn. Giữ mã nguồn và trạng thái chờ duyệt trong kết quả để người duyệt có căn cứ quyết định. Kiểm tiếp với người dùng thật xem họ có tự nhận ra cách nhập và biết phải làm gì sau khi đọc nhãn hay không.

## Kịch bản dùng thử với người ngoài nhóm · khoảng 10 phút/người

1. **Làm quen (1 phút).** Nói rõ nhóm muốn đánh giá công cụ. Mời người thử nói ra điều họ đang nghĩ.
2. **Bối cảnh (1 phút).** Hỏi lần gần nhất họ phải kiểm kịch bản hoặc quiz là khi nào và họ đã tra tài liệu ở đâu.
3. **Giao việc (1 phút).** Đưa cho người thử đoạn nháp dưới đây. Nhờ họ dùng app để quyết định câu nào có thể giữ, câu nào cần sửa và dựa vào nguồn nào. Cho họ tự thao tác trên bản chạy thật. Nếu còn thời gian, dùng B15 làm bài thứ hai.
4. **Quan sát (5 phút).** Ghi thao tác đầu tiên, cách họ dán đoạn, họ có tìm được mã nguồn và biết bước tiếp theo hay không. Khi họ kẹt, hỏi “Bạn sẽ làm gì tiếp?”.
5. **Hỏi sau (2 phút).** Hỏi điều gì khó hiểu, họ tin kết quả vì sao và nếu mai không còn công cụ thì họ thấy rất tiếc, hơi tiếc hay không sao.

Đoạn nháp giao cho người thử:

> Workflow cố định phù hợp khi các bước xử lý đã được biết trước.
>
> Trong phỏng vấn Mom Test với 3 người, hãy quy kết quả ra phần trăm và hỏi họ có thích tính năng mới không.

Người quan sát giữ đáp án đến cuối buổi. Câu đầu có căn cứ `SRC-D08-M1-01`. Câu sau mâu thuẫn với `SRC-D02-M1-01`.

## Biên bản người ngoài nhóm

Ghi một dòng sau mỗi buổi. Dùng vai trò để nhận diện người thử và chỉ ghi trích dẫn họ thực sự nói.

| Người thử (vai) | Việc giao | Quan sát | Trích nguyên văn | Mức nghiêm trọng |
|---|---|---|---|---|
| | | | | |
| | | | | |

Tổng hợp sau khi thu đủ buổi:

- Chủ đề lặp nhiều nhất:
- Sửa gì và vì sao (ghi thêm vào `spec.md` §10):
- Giữ gì và vì sao:
- Để dành sau:

## Ví dụ cách ghi

Hai dòng dưới đây minh họa cách điền nhật ký. Số buổi dùng thử đã xác nhận vẫn là 0/2.

| Người thử | Việc giao | Quan sát minh họa | Trích nguyên văn | Mức độ |
|---|---|---|---|---|
| TA từng rà bài giảng | Dùng app để quyết định câu nào nên giữ, câu nào cần sửa trong một đoạn nháp hai câu. | Dán đoạn có xuống dòng. App trả hai kết quả, người thử dừng lại để tìm kết luận chung. Sau khi tự gộp hai câu vào một dòng, họ nhận được một kết quả cho cả đoạn. | `[Ghi đúng câu họ nói lúc bị vướng]` | Vừa |
| Giảng viên từng duyệt quiz | Kiểm tra câu hỏi tương tác và tìm căn cứ để quyết định có cần sửa đề. | Đọc nhãn trước, sau đó tìm mã `SRC-...`. Họ tìm thấy mã trong kết quả nhưng chưa biết mở đoạn nguồn ở đâu để đối chiếu. | `[Ghi đúng câu họ nói khi tìm nguồn]` | Vừa |
