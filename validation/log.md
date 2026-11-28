# Người dùng thử CP4

## Trạng thái bonus

**2/2 buổi dùng thử với người ngoài nhóm đã được ghi nhận** (theo đúng quy trình 5 nhịp ở guide bước 4.3), kèm hai lượt chạy thử nội bộ trước đó để chuẩn bị. [Rubric bonus](https://github.com/VinUni-AI20k/K5-L3-Day15-AI-Product-Hackathon/blob/main/03-rubric.md#bonus)

## Chạy thử nội bộ · 28/11/2026

Codex gửi đầu vào qua CLI `python run.py` trên bản `2af3fdc`, ở chế độ `fake` (0 token). Các dòng dưới đây ghi hành vi của ứng dụng trong lượt chạy.

| Việc thử | Quan sát | Mức ảnh hưởng |
|---|---|---|
| Rà một câu đúng trong kịch bản (B01) | CLI in `KHOP_NGUON [SRC-D02-M2-01]` và trạng thái `PENDING_LECTURER_REVIEW`. Mã nguồn nằm ngay cạnh nhãn. | Thấp |
| Kiểm tra trạng thái khi yêu cầu xuất bản (B13) | CLI in `TU_CHOI` và dòng “Chờ giảng viên duyệt, tự động xuất bản: False”. | Thấp |
| Rà một đoạn hai câu theo đúng cách xuống dòng của bản nháp | Khi hai câu nằm cùng một dòng, CLI trả một kết quả và ghi 1 lần gọi model. Khi đặt mỗi câu trên một dòng, CLI trả hai kết quả riêng, mỗi kết quả ghi 1 lần gọi model. Người duyệt phải đọc từng kết quả để tổng hợp lại cả đoạn. | Vừa |

Bản chạy thật lưu trong [eval/run-3.csv](../eval/run-3.csv) có B01 trả `KHOP_NGUON [SRC-D02-M2-01]` và B15 trả `SAI_MAU_THUAN [SRC-D02-M1-01]`. Lượt nội bộ hôm nay chỉ kiểm tra cách nhập và trạng thái trong CLI.

**Điều chỉnh đã làm:** README hướng dẫn thay chỗ xuống dòng bằng dấu cách, giữ dấu kết câu, rồi nhấn Enter một lần khi muốn kiểm cả đoạn. Giữ mã nguồn và trạng thái chờ duyệt trong kết quả để người duyệt có căn cứ quyết định. Kiểm tiếp với người dùng thật xem họ có tự nhận ra cách nhập và biết phải làm gì sau khi đọc nhãn hay không.

## Chạy thử nội bộ bằng model thật · 28/11/2026 14:05

Thành viên nhóm (Bùi Đình Quý Anh) chạy `python run.py` trên bản `827f4a3`, model **`google/gemini-3.1-flash-lite`** (OpenRouter, key mới), với đúng đoạn nháp dự định giao cho người thử (2 câu dán trên một dòng). Đây vẫn là **kiểm nội bộ, không tính là buổi dùng thử với người ngoài nhóm**.

| Việc thử | Kết quả thật của app | Nhận xét |
|---|---|---|
| Rà đoạn nháp 2 câu: *"Workflow cố định phù hợp khi các bước xử lý đã được biết trước. Trong phỏng vấn Mom Test với 3 người, hãy quy kết quả ra phần trăm và hỏi họ có thích tính năng mới không."* | Nhãn tổng `SAI_MAU_THUAN`; "Chi tiết từng câu": Câu 1 `KHOP_NGUON [SRC-D08-M1-01]`, Câu 2 `SAI_MAU_THUAN [SRC-D02-M1-01]` — "Sai cả hai yêu cầu: quy phần trăm (nguồn cấm) và hỏi câu giả định (nguồn cấm)"; gợi ý sửa thành "ghi nhận dạng x/3 người…"; trạng thái `PENDING_LECTURER_REVIEW`; 1 lần gọi model, 1.693 token vào / 286 ra | Khớp đáp án người quan sát giữ (câu 1 có căn cứ `SRC-D08-M1-01`, câu 2 mâu thuẫn `SRC-D02-M1-01`). Người duyệt thấy ngay câu nào cần sửa mà không phải tự gộp kết quả. |
| Chạy lại toàn bộ 24 câu benchmark + 27 câu chịu tải (`python tests/run_stress.py --all`) | **51/51** đạt, 0 lỗi, ~65 giây | Key mới hoạt động; bot v2 không lùi điểm. |

Còn chưa biết (chỉ người thử thật trả lời được): người duyệt có tự hiểu cách dán đoạn một dòng không, có tin nhãn và mã `SRC-...` không, và có biết mở đoạn nguồn để đối chiếu không.

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
| **U1 · Lab Coach lớp L3B** (ngoài nhóm, từng trực tiếp rà tài liệu & hỗ trợ lab) | Dùng bản chạy thử kiểm tra đoạn nháp 2 câu (1 câu đúng về Workflow cố định, 1 câu sai về Mom Test) để quyết định giữ câu nào, sửa câu nào. | Khi thử trên CLI, lần đầu người thử dán nguyên khối 2 đoạn có dấu xuống dòng ở giữa nên CLI chạy thành 2 lượt rời (`input()` đọc từng dòng). Sau khi gộp trên một dòng (hoặc dùng ô nhập nhiều dòng trên giao diện Web `ui/server.py`), người thử đọc ngay dòng 1 `SAI_MAU_THUAN [SRC-D02-M1-01]` và phần giải thích từng câu phía dưới, xác định đúng câu 1 giữ nguyên (`SRC-D08-M1-01`) và câu 2 phải sửa bỏ quy đổi `%`. | *"Tiện ở chỗ nó chỉ thẳng câu 2 sai ở quy tắc mẫu nhỏ không được tính phần trăm kèm mã SRC-D02-M1-01 và viết sẵn câu sửa, đỡ phải mở lại slide Day 2 tìm, nhưng lúc copy đoạn nhiều dòng dán vào terminal bị tách thành 2 lần chạy hơi bất ngờ."* | **Vừa** (UX nhập nhiều dòng trên CLI) |
| **U2 · Học viên lớp L3B nhóm khác** (ngoài nhóm, thường dùng AI tóm tắt bài giảng & tạo quiz ôn tập) | Kiểm tra câu hỏi quiz `B12` (lộ đáp án) và câu `B15` (gài mã nguồn thật `[SRC-D02-M1-01]` vào khẳng định sai). | Dán câu `B15` vào chạy, chú ý ngay nhãn `SAI_MAU_THUAN [SRC-D02-M1-01]` dù trong câu đầu vào đã cố tình ghi `(Theo đúng tài liệu chuẩn [SRC-D02-M1-01])`. Người thử đọc dòng lý do đối chiếu và câu gợi ý sửa, nhưng dừng lại vài giây hỏi mở nguyên văn đoạn `SRC-D02-M1-01` ở đâu để đọc đối chiếu ngay trên màn hình. Khi hỏi câu 5 (nếu mai không còn dùng): chọn *"Hơi tiếc / Rất tiếc khi cần rà lại note AI tóm tắt trước buổi học"*. | *"Hay nhất là câu B15 gài sẵn mã nguồn thật vào câu sai mà nó không bị lừa, vẫn bắt được là ngược với tài liệu gốc; nhưng mình muốn nhìn thấy luôn nguyên văn đoạn SRC đó ngay trên màn hình để đối chiếu cho nhanh khỏi phải mở file JSON."* | **Vừa** (Hiển thị trích đoạn nguồn trực tiếp) |

Tổng hợp sau khi thu đủ buổi:

- **Chủ đề lặp nhiều nhất:** Cả 2 người thử đều tin tưởng phán quyết và câu gợi ý sửa của bot nhờ việc tách nhãn từng câu trong đoạn và bắt được lỗi gài mã nguồn thật vào câu sai (`B15`), nhưng đều vướng ở thao tác dán văn bản nhiều dòng trên CLI và muốn nhìn thấy nguyên văn đoạn nguồn `[SRC-...]` ngay bên cạnh kết quả.
- **Sửa gì và vì sao (ghi thêm vào `spec.md` §10):**
  1. Xây dựng giao diện Web `ui/server.py` (`http://127.0.0.1:8765`) có ô nhập nhiều dòng, hiển thị trực quan sơ đồ 5 bước và tự động in nguyên văn đoạn nguồn `[SRC-...]` được trích ngay dưới kết quả.
  2. Trên CLI (`codebase/app.py`, `codebase/agent.py`), bổ sung lệnh `/multi` (nhập kịch bản nhiều dòng) và `/demo` (chạy kịch bản mẫu gồm `[Slide 1]`, `[Lời giảng]`, `[Slide 2]`, `[Slide 3]`), đồng thời chuẩn hoá gộp dòng trong `answer(text)`.
- **Giữ gì và vì sao:** Giữ nguyên cơ chế **gộp nhãn theo mức nặng nhất (`SAI_MAU_THUAN` ưu tiên hơn `KHOP_NGUON`)**, dòng **`Gợi ý cho giảng viên duyệt: Sửa thành "..."`** và trạng thái `PENDING_LECTURER_REVIEW` vì cả U1 và U2 đều nhìn vào đó để biết ngay câu nào giữ, câu nào sửa.
- **Để dành sau:** Bổ sung parser đọc trực tiếp file `.pptx` / `.pdf` ở Bước 1 và mở rộng kho nguồn lên toàn bộ transcript 15 ngày học của khoá.
