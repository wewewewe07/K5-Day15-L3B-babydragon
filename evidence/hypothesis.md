# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.

- Ngày giờ viết: 27/11/2026 16:50
- Người dùng chính (một vai cụ thể): **Giảng viên / Thành viên đội sản xuất và kiểm duyệt bài giảng online (pre-class) của khoá AI20K** (cùng người chịu ảnh hưởng trực tiếp khi bài giảng thiếu/lệch thông tin là học viên L3 học trên trang pre-class).
- **Mình nghĩ:** Giảng viên và đội sản xuất bài giảng online gặp khó khi phải kiểm và duyệt kịch bản lời giảng cũng như các câu hỏi tương tác do AI sinh (30–50 câu/bài) vì văn bản AI viết rất trôi chảy nhưng hay cài cắm các khẳng định không có trong tài liệu nguồn, lệch định nghĩa tinh vi, hoặc câu hỏi tương tác bị lộ đáp án/mơ hồ; hậu quả là người duyệt mất 1–2 giờ đọc dò từng câu với tài liệu gốc cho mỗi bài giảng, và những chỗ sót lỗi khiến hàng trăm học viên trên trang pre-class trả lời sai hoặc phải bấm hỏi trợ giảng AI liên tục.
- **Có thể còn cách giải thích khác:** Bản nháp bài giảng và câu hỏi do model sinh ra đã đúng sẵn >95% từ đầu, giảng viên chỉ cần đọc lướt trong 10 phút mà không cần đối chiếu từng khẳng định với nguồn.
- **Mình đúng nếu thấy:**
  1. Từ phỏng vấn: **≥2/3 thành viên đội sản xuất bài giảng / giảng viên / TA** xác nhận khâu kiểm chứng kiến thức & đối chiếu nguồn cho kịch bản/câu hỏi pre-class chiếm nhiều thời gian nhất và từng phát hiện lỗi sai tinh vi / thiếu căn cứ trước hoặc sau khi đăng bài.
  2. Từ đào dữ liệu thật (`data/preclass/`): Tìm thấy bằng chứng định lượng (`x/N` và `%`) về các đoạn bài giảng / câu hỏi thực tế trên hệ thống bị học viên hỏi dồn do thiếu ngữ cảnh (`missing_context = True` ở `agent_replied`) hoặc tỷ lệ trả lời sai lần đầu cao bất thường ở một số bài học/module cụ thể.
- **Nguồn sẽ dùng** (≥1 nguồn đạt ngưỡng, guide 1.2): [x] đào data · [x] phỏng vấn ≥3 · [x] khảo sát ≥20 — **nguồn chính:** Phỏng vấn ≥3 người trong đội sản xuất bài giảng / giảng viên / TA + Đào dữ liệu nhật ký hành vi thật `data/preclass/` · **nguồn để kiểm lại:** Khảo sát học viên lớp L3B về các chỗ bài giảng/câu hỏi pre-class gây hiểu nhầm hoặc thiếu căn cứ.
