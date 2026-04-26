# Translator Desktop App

Ứng dụng dịch thuật tài liệu chuyên nghiệp sử dụng AI (Google Gemini, OpenAI, Anthropic). Hỗ trợ dịch file Docx giữ nguyên định dạng và quản lý thuật ngữ (Glossary).

## ✨ Tính năng chính

- **Dịch file Docx**: Giữ nguyên định dạng (Bold, Italic, Tables) nhờ sử dụng Markdown làm trung gian.
- **Đa nền tảng AI**: Hỗ trợ Google Gemini, OpenAI và Anthropic.
- **Quản lý thuật ngữ (Glossary)**: Tự động trích xuất và áp dụng thuật ngữ chuyên ngành khi dịch.
- **Quy trình 2 bước**: Dịch (Translate) và Hiệu đính (Review) để đảm bảo chất lượng văn phong cao nhất.
- **Giao diện hiện đại**: Xây dựng bằng `customtkinter` trực quan, dễ sử dụng.

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống
- Python 3.10 trở lên.
- **Pandoc**: Cần thiết để xử lý định dạng Docx. Tải tại [pandoc.org](https://pandoc.org/installing.html).

### 2. Cài đặt môi trường
1. Clone dự án:
   ```bash
   git clone <link-your-repo>
   cd Translator
   ```
2. Tạo môi trường ảo (venv):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   ```
3. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Cấu hình
1. Copy file `.env.example` thành `.env`:
   ```bash
   cp .env.example .env
   ```
2. Điền các API Key của bạn vào file `.env` hoặc cấu hình trực tiếp trong phần **Settings** của ứng dụng.

## 🛠️ Cách sử dụng

1. Chạy ứng dụng:
   ```bash
   python main.py
   ```
2. **Cài đặt**: Nhập API Key và chọn Model mong muốn.
3. **Dịch thuật**: Kéo thả file Docx vào, chọn lĩnh vực và nhấn nút Dịch.
4. **Kiểm tra Model**: Chạy `python check_models.py` để xem các model khả dụng với API Key của bạn.

## 📁 Cấu trúc thư mục

- `core/`: Chứa logic xử lý file, AI engine và quản lý cấu hình.
- `ui/`: Chứa mã nguồn giao diện người dùng (CustomTkinter).
- `data/`: Lưu trữ database thuật ngữ và file cấu hình.
- `test/`: Các kịch bản kiểm thử (Unit tests).

## 📄 Giấy phép
Dự án này được phát triển cho mục đích học tập và làm việc cá nhân.

---
*Phát triển bởi [Tên của bạn/Antigravity]*
