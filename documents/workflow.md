# Giải pháp Dịch thuật Tài liệu Docx (Nhật -> Việt)

Đây là đề xuất kiến trúc và luồng xử lý (workflow) cho dự án Translator nhằm đáp ứng 3 yêu cầu cốt lõi của bạn: mapping câu-câu, thống nhất thuật ngữ, và giữ nguyên định dạng.

## 1. Luồng xử lý tổng thể (Workflow)

Hệ thống sẽ hoạt động theo 4 bước chính:

1. **Bóc tách & Chuyển đổi Đoạn văn sang Markdown (Hybrid Conversion):** 
   - Duyệt từng đoạn văn (paragraph) trong `.docx`.
   - Sử dụng Pandoc để chuyển đổi nội dung của chính đoạn văn đó sang định dạng Markdown (giữ lại in đậm, in nghiêng, tiêu đề).
2. **Smart Batching & AI Translation:**
   - Chia danh sách đoạn văn thành các khối (mặc định gộp để đạt 5 câu hoặc tối đa 5 đoạn).
   - **Gộp thông minh**: Đoạn ngắn (< 5 câu) sẽ tự động gộp vào đoạn sau để đảm bảo đủ ngữ cảnh cho AI.
   - **Xử lý Tiêu đề**: Tiêu đề `【 】` sẽ gộp luôn nội dung ngắn ngay sau nó vào cùng một khối để AI hiểu đúng ngữ cảnh.
   - **Hiển thị Auto-height**: Trên giao diện, các đoạn văn được hiển thị full nội dung để người dùng rà soát thuận tiện nhất.
3. **Quản lý Thuật ngữ (Glossary) & AI Analysis:**
   - **Tự động nhận diện**: Hệ thống tự động phân tích lĩnh vực của tài liệu ngay khi nạp file.
   - **Tự động trích xuất & Dừng Review**: Sau khi nhận diện lĩnh vực, hệ thống tự động trích xuất thuật ngữ và hiển thị một màn hình Review. Người dùng bắt buộc phải xác nhận/chỉnh sửa danh sách này trước khi tiến trình dịch toàn văn được phép bắt đầu.
   - **Bảo toàn dữ liệu cũ**: Nếu thuật ngữ đã tồn tại trong Glossary, hệ thống sẽ bỏ qua và giữ nguyên bản dịch cũ; nếu chưa có, hệ thống mới tiến hành dịch và thêm vào.
   - **Lọc thuật ngữ động (Smart Filtering)**: Khi dịch từng đoạn, hệ thống chỉ gửi các thuật ngữ thực sự xuất hiện trong đoạn đó cho AI.
   - **Sidebar thuật ngữ theo trang**: Thanh bên chỉ hiển thị các thuật ngữ xuất hiện trong trang (khối văn bản) hiện tại và tự động làm mới khi người dùng chuyển trang, giúp tập trung tối đa vào nội dung đang rà soát.
4. **Tái tạo tài liệu (Hybrid Reconstruction):**
   - Chuyển ngược từng đoạn Markdown đã dịch về định dạng Word.
   - Thay thế các "run" văn bản trong đoạn cũ bằng các "run" mới đã được định dạng.
   - Giữ nguyên style tổng thể, căn lề và các thành phần không phải văn bản (ảnh, bảng) của file gốc.

---

## 2. Giải pháp Kỹ thuật cho Từng Yêu Cầu

### Yêu cầu 1: Các câu dịch ra phải mapping với câu ở bên tài liệu cũ
- **Vấn đề:** Trong tài liệu dịch, nếu chỉ dịch tự động thẳng ra file cuối thì người dùng khó đối chiếu xem AI dịch có đúng không. 
- **Giải pháp:** Hệ thống có thể hỗ trợ sinh ra một file trung gian (ví dụ file Excel, hoặc file JSON song ngữ) gồm 2 cột "Tiếng Nhật - Tiếng Việt". Bạn có thể xem lại file này để tinh chỉnh, sau đó hệ thống mới tiếp tục quy trình nhúng tiếng Việt vào file Word.

### Yêu cầu 2: Các thuật ngữ chuyên môn được dịch thống nhất & Lưu lại
- **Giải pháp:** Xây dựng module **Glossary**.
  - **Lưu trữ:** Tạo file `glossary.json` hoặc SQLite chứa các cặp `{"ja": "thuật ngữ", "vi": "nghĩa"}`.
  - **Sử dụng:** Prompt gửi cho AI sẽ có dạng: *"Bạn là một dịch giả chuyên nghiệp. Dịch đoạn văn sau từ tiếng Nhật sang tiếng Việt. BẮT BUỘC sử dụng các thuật ngữ sau: [X] dịch là [Y]..."*
  - **Mở rộng:** Cung cấp tính năng thêm thuật ngữ mới vào database qua từng lần dịch để làm giàu vốn từ.

### Yêu cầu 3: Giữ nguyên định dạng tài liệu gốc
- **Giải pháp:** Chúng ta sẽ **không** tạo một file Word mới tinh.
- Thay vào đó, chúng ta mở file Docx gốc bằng code, tìm đến các chuỗi văn bản (text property của các Run/Paragraph), **thay thế phần text tiếng Nhật bằng text tiếng Việt**, và `Save As` sang một file mới. Bằng cách này, 100% định dạng khung, bảng, ảnh, font sẽ được bảo toàn.

### Yêu cầu 4: Tiếp tục tiến trình khi gặp lỗi hoặc tạm dừng
- **Giải pháp**: Xây dựng module **Progress Manager**.
  - Khi bắt đầu làm việc với một file `.docx`, hệ thống kiểm tra sự tồn tại của file tiến trình tương ứng trong `data/progress/`.
  - Nếu có, hệ thống nạp lại các bản dịch cũ và hiển thị lên giao diện.
  - Khi người dùng nhấn "Bắt đầu dịch", hệ thống chỉ gửi những đoạn chưa có bản dịch lên AI API.
  - Trong quá trình Human Review, người dùng có thể nhấn "Lưu Bản Nháp" để ghi lại các chỉnh sửa thủ công vào file tiến trình.

---

## Open Questions (Cần thảo luận)

Để tôi có thể thiết lập mã nguồn chính xác nhất, bạn hãy giúp tôi làm rõ các điểm sau:
1. **Ngôn ngữ lập trình:** Bạn có quen thuộc và muốn viết dự án này bằng ngôn ngữ nào không? (Tôi đề xuất **Python** vì hệ sinh thái hỗ trợ xử lý Docx và AI rất mạnh).
2. **Giao diện sử dụng:** Bạn muốn công cụ này chạy trên Dòng lệnh (CLI command), có Giao diện máy tính (Desktop App), hay là một Web App nội bộ?
3. **Tính năng duyệt lại (Review):** Bạn có muốn công cụ sinh ra một file song ngữ tạm thời (Excel/CSV) để bạn có thể chỉnh sửa câu dịch bằng tay trước khi xuất ra file Word cuối cùng không?
