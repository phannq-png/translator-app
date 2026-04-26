# Báo cáo Tiến độ Phát triển (Project Progress Log)
Cập nhật lần cuối: 2026-04-25

## 1. Công việc đã Hoàn thành (Completed)

### 核心 Core Processing
- [x] **Hybrid Paragraph-to-Markdown**: Bóc tách đoạn văn đơn lẻ sang Markdown để bảo toàn 100% định dạng Word.
- [x] **Smart Chunking (v4 - Enhanced)**: 
    - **Gộp đoạn ngắn**: Tự động gộp các đoạn văn vào khối tiếp theo nếu tổng số câu < 5 (đảm bảo ngữ cảnh cho AI).
    - **Giới hạn vật lý**: Tối đa 5 đoạn văn mỗi khối để tránh quá tải token.
    - **Xử lý Tiêu đề 【 】 thông minh**: 
        - Tiêu đề sẽ không bị tách rời nếu đoạn văn ngay sau nó chỉ có 1 câu.
        - Chỉ cho phép ngắt khối khi gặp tiêu đề nếu khối hiện tại đã đạt ít nhất 3 câu (tránh khối mồ côi).
- [x] **Asynchronous Loading**: Chuyển việc bóc tách file sang luồng nền, không gây treo UI.
- [x] **AI Engine**: 
    - Tích hợp Gemini API dịch thuật trực tiếp trên Markdown.
    - [x] **Smart Terminology**: 
    - Tự động lọc thuật ngữ theo từng trang.
    - **Sidebar thuật ngữ**: Hiển thị và cho phép sửa nhanh thuật ngữ ngay tại màn hình chính, đồng bộ theo trang.
    - **Màn hình Review bắt buộc**: Bước dừng để người dùng duyệt thuật ngữ trước khi dịch.
- [x] **Manual & Active Control**:
    - Chuyển sang chế độ dịch từng trang theo ý muốn của người dùng.
    - **Prompt Tools**: Cung cấp công cụ lấy Prompt dịch và Prompt review để sử dụng với AI bên ngoài.
- [x] **Data Integrity**: Ngăn chặn trùng lặp thuật ngữ bằng cơ chế chuẩn hóa dữ liệu tự động.

### 界面 UI/UX
- [x] **Active Sidebar**: Thanh bên hiển thị thuật ngữ linh hoạt.
- [x] **Terminology Review UI**: Giao diện kiểm duyệt thuật ngữ chuyên nghiệp trước khi dịch.
- [x] **Prompt Popups**: Giao diện hiển thị và copy Prompt nhanh chóng.
- [x] **Pagination (Phân trang)**: Hiển thị 1 khối/trang với nút điều hướng Prev/Next.
- [x] **Auto-save on Navigate**: Tự động lưu dữ liệu vào bộ nhớ khi chuyển trang.
- [x] **Loading Overlay & Spinner**: Thêm màn hình chờ với vòng xoay Spinner chuyên nghiệp (Pillow-based rotation).
- [x] **Layout Optimization**: 
    - Cố định Footer ở đáy màn hình.
    - Ghim thanh điều hướng trang ở đáy khung nội dung.
- [x] **Progress Feedback**: Thanh tiến trình bóc tách (%) và thông báo trạng thái mượt mà.

## 2. Trạng thái Hiện tại (Current Status)
- **Phiên bản**: Beta v0.8
- **Tính ổn định**: Cao. Quy trình dịch thuật chủ động giúp người dùng kiểm soát 100% chất lượng.
- **Tính năng nổi bật**: Hệ thống lấy Prompt thông minh giúp tối ưu hóa việc sử dụng các model AI mạnh mẽ bên ngoài (GPT-4, Claude 3.5...).

## 3. Kế hoạch Tiếp theo (Next Steps)
- [ ] Hoàn thiện tính năng Kéo-Thả file (Drag & Drop) một cách ổn định nhất trên Windows.
- [ ] Thêm tính năng "Dịch hàng loạt" (Batch) dành cho các trang đã được Review.
- [ ] Xuất báo cáo thuật ngữ (Glossary Report) ra file Excel/CSV.
