# Yêu cầu Dự án (Project Requirements) - Translator Desktop App

## 1. Tổng quan Dự án
- **Loại ứng dụng**: Desktop Application.
- **Ngôn ngữ phát triển**: Python.
- **Giao diện người dùng (UI)**: Thư viện tạo UI hiện đại cho Python (CustomTkinter/PyQt).
- **Công nghệ cốt lõi**: `python-docx`, `Pandoc` (qua `pypandoc`) để xử lý văn bản trung gian và **Google AI API** (Gemini) để dịch thuật.

## 2. Các Tính năng Chính (Core Features)

### 2.1. Xử lý Tài liệu Docx & Giao diện Phân trang
- **Hybrid Paragraph-to-Markdown**: Từng đoạn văn được xử lý riêng biệt bằng Pandoc để bảo toàn layout gốc 100%.
- **Giao diện Phân trang (Pagination)**: Thay vì danh sách cuộn dài, ứng dụng hiển thị theo từng trang (mỗi trang là một khối văn bản). Hỗ trợ điều hướng "Trang trước/sau".
- **Smart Title-aware Chunking**: Tự động nhận diện dấu `【 】` để ngắt trang, đảm bảo tiêu đề luôn nằm ở đầu trang.
- **Xử lý Bất đồng bộ (Async)**: Load file và dịch thuật chạy trên luồng riêng, có thanh tiến trình (Progress Bar) để tránh treo UI.

### 2.2. Quản lý Thuật ngữ (Glossary)
- **Phân loại theo lĩnh vực**: Glossary được chia thành nhiều nhóm khác nhau tùy theo lĩnh vực. Trước khi dịch, hệ thống (thông qua AI) sẽ tự động phân tích văn bản để **nhận diện lĩnh vực**. 
- **Tự động thêm Lĩnh vực mới**: Nếu tài liệu thuộc một lĩnh vực hoàn toàn mới chưa từng có trong hệ thống, AI sẽ tự động định danh lĩnh vực đó và thêm vào danh sách quản lý.
- **Tối ưu hóa Token**: Hệ thống sử dụng các kỹ thuật rút gọn Prompt và giới hạn độ dài văn bản đầu vào cho bước nhận diện lĩnh vực để tiết kiệm chi phí tối đa.
- **Cơ chế hoạt động**: Thuật ngữ chuyên ngành sẽ được tự động trích xuất từ tài liệu hiện tại.
- **Quy trình trích xuất & cập nhật**:
  - Hệ thống kiểm tra xem thuật ngữ đã có trong bộ Glossary của lĩnh vực đó hay chưa.
  - Nếu **đã có**, hệ thống sẽ sử dụng ngay nghĩa tiếng Việt đang lưu để đưa vào ngữ cảnh (Prompt) dịch.
  - Nếu **chưa có**, hệ thống sẽ gọi API để tự động dịch thuật ngữ đó sang tiếng Việt, sau đó lưu (update dần dần) vào Glossary của lĩnh vực hiện tại để tái sử dụng.
- **Lưu trữ**: Bộ từ điển lưu dưới dạng file `glossary.json` (chia cấu trúc theo lĩnh vực) hoặc database `SQLite` (có thêm cột `domain`).
- **Giao diện quản lý**: Sẽ có một màn hình phụ (Secondary Window) để Quản lý Thuật ngữ. Người dùng nếu có nhu cầu có thể mở lên để xem danh sách lĩnh vực và thao tác Thêm/Sửa/Xóa thuật ngữ thủ công, không làm cản trở luồng dịch chính.

### 2.3. Pipeline Dịch thuật và Review (Markdown trung gian)
Luồng xử lý văn bản sẽ đi qua các bước:
1. **Chuyển đổi Docx -> Markdown**: Dùng Pandoc để trích xuất văn bản sang Markdown nhằm tối ưu token và giữ cấu trúc (heading, list, bold).
2. **Xử lý Word & Định dạng trung gian:** `python-docx` và `Pandoc`. Sử dụng phương pháp **Hybrid Paragraph-to-Markdown**: Từng đoạn văn được xử lý riêng biệt để bảo toàn layout gốc 100%.
- **Giao diện Review thông minh:** Tự động giãn chiều cao (Auto-height) cho các ô nhập liệu giúp quan sát trọn vẹn nội dung đoạn văn dài mà không cần cuộn bên trong ô.
- **AI Engine:** Google GenAI (Gemini API) - Dịch thuật trên định dạng Markdown.
3. **Human Review (Người dùng xác nhận trên App)**: Hiển thị các đoạn Markdown dịch lên UI để người dùng kiểm tra/sửa đổi.
4. **Export (Xuất file)**: Dùng Pandoc chuyển ngược Markdown dịch về `.docx` để tạo file kết quả.

### 2.4. Quản lý Cấu hình AI Đa Nền Tảng (3 Giai đoạn chuyên biệt)
- **Hỗ trợ Đa Provider**: Cho phép người dùng lựa chọn giữa **Google Gemini, OpenAI (ChatGPT) và Anthropic (Claude)**.
- **Tách biệt 3 tác vụ AI**: Để tối ưu hóa chi phí và chất lượng, hệ thống cho phép cấu hình Model riêng cho:
    1. **AI Nhận diện Lĩnh vực (Detector)**: Chuyên phân loại tài liệu (Khuyên dùng các dòng Flash Lite để tiết kiệm token).
    2. **AI Dịch thuật (Translator)**: Chuyên chuyển ngữ nội dung chính.
    3. **AI Kiểm duyệt (Reviewer)**: Chuyên chuốt lại văn phong (Khuyên dùng các dòng Pro/Opus để có chất lượng cao nhất).
- **Hỗ trợ Model mới nhất**: Tích hợp sẵn danh sách các model mới nhất như Gemini 3, 2.5, 2.0 (Flash, Pro, Flash-Lite).
- **Giao diện Cài đặt (Setup Screen)**: 
    - Giao diện dạng cuộn (Scrollable) chứa 3 phân vùng cấu hình riêng biệt.
    - Cho phép chọn Provider, nhập API Key trực tiếp, và chọn Model từ dropdown hoặc tự nhập.
- **Export & Import**: Tính năng xuất/nhập cấu hình API ra file JSON.

### 2.5. Quản lý Tiến trình và Smart Chunking
- **Fixed Batching & Pagination**: Hiển thị cố định 1 khối văn bản trên mỗi trang. Tự động lưu bản dịch khi chuyển trang.
- **Quy tắc Gộp Thông minh**: 
    - **Tối thiểu 5 câu**: Gộp các đoạn ngắn để AI có đủ ngữ cảnh và người dùng rà soát hiệu quả.
    - **Tối đa 5 đoạn**: Không gộp quá 5 đoạn văn vào một khối để tránh trang bị quá dài.
- **Title-aware logic (Hard Start)**: Các đoạn văn bắt đầu bằng `【 】` luôn được coi là điểm khởi đầu của một khối mới. Không gộp ngược tiêu đề vào khối phía trước.
- **Loading Progress**: Hiển thị thanh tiến trình (%) và Spinner xoay mượt mà khi bóc tách file Word. Luồng xử lý nền giúp UI luôn phản hồi mượt mà.
- **Bảo toàn Cấu trúc**: Hệ thống tự động ánh xạ (mapping) và lắp ráp lại các khối văn bản về đúng cấu trúc file Word gốc.
- **Lưu Tiến trình**: Lưu bản dịch theo các khối Chunk để có thể khôi phục nhanh chóng.
- **Lưu Nháp Thủ công**: Cho phép người dùng chủ động lưu lại các chỉnh sửa (Human Review) bất cứ lúc nào để tiếp tục sau này.

## 3. Kiến trúc Luồng Dữ liệu (Data Flow)
1. User chọn file `.docx`.
2. App trích xuất danh sách các câu tiếng Nhật.
3. App gọi AI API đọc lướt nội dung để **nhận diện lĩnh vực** của tài liệu và chọn bộ Glossary phù hợp.
4. App quét danh sách thuật ngữ xuất hiện trong các câu dựa trên Glossary của lĩnh vực đã chọn.
5. App gọi AI API -> Dịch (Draft 1).
5. App gọi AI API -> Review (Draft 2 - Bản hoàn thiện từ AI).
6. App hiển thị Draft 2 lên màn hình chính.
7. User kiểm tra và sửa đổi trên giao diện (Final Draft).
8. App build file `.docx` mới từ Final Draft.
