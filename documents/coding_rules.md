# Quy tắc Viết Code (Coding Rules / Conventions)

Tài liệu này quy định các tiêu chuẩn và nguyên tắc viết mã nguồn cho toàn bộ thành viên (bao gồm cả AI và con người) tham gia phát triển dự án **Translator Desktop App**. Mục đích là để giữ cho code luôn sạch, dễ đọc, dễ bảo trì và mở rộng.

## 1. Quy tắc Đặt tên (Naming Conventions)
- **Ngôn ngữ**: Toàn bộ Tên biến, Tên hàm, Tên Class và Tên file BẮT BUỘC phải viết bằng **Tiếng Anh** để đảm bảo code chuẩn quốc tế và dễ đọc. (Ví dụ: dùng `file_path` thay vì `duong_dan_file`).
- Tuân thủ chặt chẽ tiêu chuẩn **PEP 8** của Python:
- **Biến (Variables) & Hàm (Functions)**: Viết thường, phân tách bằng dấu gạch dưới (`snake_case`).
  - *Ví dụ đúng*: `extracted_text`, `get_glossary()`, `translate_sentence()`
- **Hằng số (Constants)**: Viết hoa toàn bộ, phân tách bằng dấu gạch dưới (`UPPER_SNAKE_CASE`).
  - *Ví dụ đúng*: `MAX_RETRIES = 3`, `GEMINI_MODEL = "gemini-1.5-pro"`
- **Lớp (Classes)**: Viết hoa chữ cái đầu mỗi từ (`PascalCase`).
  - *Ví dụ đúng*: `DocxProcessor`, `AiEngine`, `MainApp`
- **Tên File/Thư mục (Files & Folders)**: Viết thường, có thể dùng dấu gạch dưới (`snake_case.py`).

## 2. Kiến trúc và Cấu trúc Code
- **Tuyệt đối tách biệt UI và Core (SoC - Separation of Concerns)**:
  - Thư mục `/core` CHỈ xử lý dữ liệu và logic (không bao giờ được gọi các thư viện vẽ giao diện như `customtkinter` ở đây). Các hàm trong `/core` chỉ nhận tham số đầu vào và `return` kết quả hoặc ném lỗi (`raise Exception`).
  - Thư mục `/ui` CHỈ xử lý sự kiện click chuột và hiển thị dữ liệu lên màn hình.
- **Tránh hard-code**: Mọi thông số nhạy cảm (API Key) hoặc đường dẫn cấu hình phải được nạp qua file `.env` hoặc file config.

## 3. Comments và Tài liệu (Documentation)
- **Docstrings**: BẮT BUỘC phải viết Docstring (mô tả hàm) cho mọi function và class quan trọng. Định dạng theo Google Style.
  ```python
  def extract_text(file_path: str) -> list:
      """
      Bóc tách văn bản từ file Word (.docx).

      Args:
          file_path (str): Đường dẫn tuyệt đối đến file cần xử lý.

      Returns:
          list: Danh sách các đối tượng chứa thông tin văn bản và index.
      """
  ```
- **Ngôn ngữ Comment**: Thống nhất viết comment bằng **Tiếng Việt** để sát với ngữ cảnh nghiệp vụ đã thảo luận. Comment để giải thích **TẠI SAO** làm vậy (Why), chứ không phải giải thích code đó làm gì (What).

## 4. Xử lý Lỗi (Error Handling)
- Luôn bọc các đoạn code thao tác với File (đọc/ghi Word) và Gọi API (truyền thông tin mạng) trong khối `try...except`.
- Không bao giờ dùng `except Exception as e: pass` (nuốt lỗi một cách im lặng). Phải log lỗi ra màn hình terminal hoặc đưa một thông báo lỗi (Error MessageBox) lên UI để người dùng biết.
- Với các lỗi liên quan đến API Rate Limit của Google, cần tích hợp cơ chế Retry (thử lại) hoặc thông báo rõ ràng cho người dùng chờ.

## 5. Định dạng Code (Formatting)
- Sử dụng **Black** làm formatter chuẩn. Code trước khi lưu cần được format bởi Black (độ dài tối đa một dòng: 88 ký tự).
- Giữ code gọn gàng: Xóa bỏ mọi hàm `print()` debug dư thừa hoặc các thư viện được `import` nhưng không sử dụng trước khi commit.
