# Tài liệu Kỹ thuật & Thiết lập Môi trường (Technical & Setup Guide)

Tài liệu này mô tả chi tiết các yêu cầu về hệ thống, môi trường và các thư viện kỹ thuật cần thiết để chạy dự án **Translator Desktop App**.

## 1. Môi trường Yêu cầu (Prerequisites)
Để chạy được mã nguồn của dự án này, máy tính của bạn cần được cài đặt sẵn các phần mềm sau:
- **Python**: Phiên bản `3.10` trở lên (Khuyến nghị 3.11 hoặc 3.12).
- **Hệ điều hành**: Windows 10/11, macOS, hoặc Linux.
- **Tài khoản Google AI Studio**: Cần có một `API Key` hợp lệ của Google Gemini để sử dụng tính năng dịch thuật và AI.

## 2. Các Thư viện Kỹ thuật (Dependencies)
Dự án sử dụng các thư viện mã nguồn mở sau (sẽ được liệt kê trong file `requirements.txt`):

1. **`customtkinter`**: 
   - **Mục đích**: Xây dựng giao diện người dùng (Desktop GUI).
   - **Lý do sử dụng**: Cung cấp các component hiện đại, bo góc đẹp mắt và hỗ trợ Dark/Light mode tự động, vượt trội hơn Tkinter truyền thống.

2. **`python-docx`**:
   - **Mục đích**: Đọc, bóc tách văn bản và ghi đè nội dung file `.docx`.
   - **Lý do sử dụng**: Khả năng can thiệp sâu vào cấu trúc XML của file Word, giúp giữ nguyên 100% định dạng ban đầu (bảng biểu, in đậm, màu sắc...).

3. **`google-genai`** (hoặc `google-generativeai`):
   - **Mục đích**: Giao tiếp với Google Gemini API.
   - **Lý do sử dụng**: Đóng vai trò là "Bộ não" của hệ thống để phân tích lĩnh vực tài liệu, dịch văn bản theo ngữ cảnh và tự động review kết quả.

4. **`python-dotenv`**:
   - **Mục đích**: Đọc biến môi trường từ file `.env`.
   - **Lý do sử dụng**: Giúp bảo mật API Key của Google, tránh việc hard-code key trực tiếp vào mã nguồn.

5. **`sqlite3`** (Có sẵn trong thư viện chuẩn của Python):
   - **Mục đích**: Lưu trữ Database nội bộ cho bộ từ điển (Glossary).
   - **Lý do sử dụng**: Gọn nhẹ, không cần cài đặt server CSDL riêng, hỗ trợ truy vấn cấu trúc dữ liệu theo lĩnh vực (domain) cực nhanh.

## 3. Hướng dẫn Cài đặt (Installation Steps)

**Bước 1: Clone hoặc tải mã nguồn về máy**
Di chuyển vào thư mục dự án trên Terminal/Command Prompt.

**Bước 2: Tạo môi trường ảo (Virtual Environment) - Khuyến nghị**
Việc dùng môi trường ảo giúp các thư viện của dự án không xung đột với các ứng dụng Python khác trên máy bạn.
```bash
python -m venv venv
```

**Bước 3: Kích hoạt môi trường ảo**
- Trên Windows:
  ```bash
  venv\Scripts\activate
  ```
- Trên macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

**Bước 4: Cài đặt các thư viện yêu cầu**
```bash
pip install customtkinter python-docx google-generativeai python-dotenv
```
*(Lưu ý: Sau này hệ thống sẽ có file `requirements.txt`, lệnh cài đặt sẽ là `pip install -r requirements.txt`)*

## 4. Thiết lập API Key
1. Tại thư mục gốc của dự án, tạo một file tên là `.env`.
2. Mở file `.env` và dán API Key của Google vào theo định dạng sau:
   ```env
   GEMINI_API_KEY=AIzaSyB..._your_api_key_here...
   ```

## 5. Khởi chạy Ứng dụng
Sau khi đã hoàn tất các bước trên, bạn khởi chạy ứng dụng bằng lệnh:
```bash
python main.py
```
Giao diện ứng dụng Translator sẽ lập tức hiện lên.
