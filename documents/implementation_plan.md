# Kế hoạch triển khai (Implementation Plan) - Translator Desktop App

Dự án Translator Desktop App là một công cụ hỗ trợ dịch thuật tự động giữ nguyên định dạng file `.docx` từ tiếng Nhật sang tiếng Việt, kết hợp tính năng quản lý thuật ngữ thông minh theo lĩnh vực.

## 1. Kiến trúc Tổng thể (Architecture)

**Công nghệ sử dụng:**
- **Ngôn ngữ:** Python 3.10+
- **Giao diện (UI):** `customtkinter` (Giao diện hiện đại, hỗ trợ Dark/Light mode).
- **Xử lý Word (.docx):** `python-docx` (Trích xuất văn bản, giữ nguyên định dạng, bảng biểu, hình ảnh).
- **AI Engine:** Google GenAI (Gemini API) - Đóng vai trò vừa nhận diện lĩnh vực, vừa dịch thuật, vừa review câu dịch tự động.
- **Lưu trữ dữ liệu:** `SQLite` (hoặc `json`) dùng cho từ điển thuật ngữ (`glossary`).

## 2. Thiết kế Giao diện (UI Design)

Ứng dụng sẽ có giao diện tập trung vào luồng dịch thuật, kèm theo một màn hình phụ:

1. **Màn hình Chính (Dịch thuật & Review):**
   - Khu vực Upload file `.docx` (Tự động khôi phục tiến trình dịch nếu trước đó đã làm dở).
   - Bảng/Danh sách đối chiếu (Table): Hiển thị từng câu **Gốc (Tiếng Nhật) | Bản dịch (AI đã duyệt) | Chỉnh sửa cuối (Human)**.
   - Nút "Bắt đầu dịch" (Tự động bỏ qua các câu đã dịch, chỉ dịch tiếp các câu còn trống).
   - Nút "Lưu Bản Nháp" (Save Progress) để lưu lại các câu mà con người vừa chỉnh sửa.
   - Nút "Xác nhận & Xuất File" (Ghi đè bản dịch vào docx và Save As).
   - Nút mở màn hình phụ "Quản lý Thuật ngữ" (Dành cho người dùng muốn chỉnh sửa nâng cao).

2. **Màn hình Phụ (Quản lý Thuật ngữ):**
   - Mở dưới dạng Secondary Window / Dialog khi người dùng cần.
   - Quản lý lĩnh vực và Thêm mới, Sửa, Xóa cặp từ Nhật - Việt.

3. **Màn hình Phụ (Cài đặt Đa AI & API Keys):**
   - Hỗ trợ chọn **Provider** (Google, OpenAI, Anthropic) cho **3 tác vụ riêng biệt**: Nhận diện lĩnh vực, Dịch thuật, và Review.
   - Giao diện dạng cuộn (Scrollable Frame) để quản lý nhiều cấu hình.
   - Danh sách Model gợi ý phong phú (bao gồm Gemini 3, 2.5, 2.0 Flash-Lite).
   - Chức năng Export/Import cài đặt ra file JSON.

## 3. Các Module Chính (Proposed Changes / Code Structure)

### Khởi tạo Dự án
Dự án sẽ gồm các thư mục và file sau:

#### [NEW] `requirements.txt`
Danh sách thư viện: `customtkinter`, `python-docx`, `google-genai`, `python-dotenv`.

#### [NEW] `main.py`
Entry point của ứng dụng, khởi tạo và quản lý giao diện chính bằng `customtkinter`. Chứa logic điều hướng giữa màn hình Dịch thuật và màn hình Quản lý thuật ngữ.

#### [NEW] `ui_glossary.py`
Chứa toàn bộ mã nguồn xây dựng giao diện "Màn hình Quản lý Thuật ngữ".

#### [NEW] `ui_settings.py`
Chứa mã nguồn xây dựng "Màn hình Cài đặt AI & API Keys".

#### [NEW] `core/docx_processor.py`
- Hàm `extract_text()`: Bóc tách text, đánh index.
- Hàm `reconstruct_document()`: Ghi đè vào file gốc theo đúng index.

#### [NEW] `core/config_manager.py`
- Quản lý `config.json` (Export, Import, Load API Key theo loại AI).

#### [NEW] `core/ai_engine.py`
Lấy cấu hình từ `config_manager` để gọi các AI tương ứng.
**Sẽ áp dụng Factory Pattern** để hỗ trợ nhiều Provider:
- `_generate_content(prompt, provider, api_key, model)`: Factory method định tuyến yêu cầu đến đúng thư viện của nhà cung cấp.
- `detect_domain()`: Sử dụng cấu hình từ bộ **Detector**.
- `translate_and_review(sentences: list[str], ...)`: Hỗ trợ dịch và review theo nhóm (batch) câu để tối ưu token. Sử dụng định dạng đánh số `[1], [2]...` để phân tách kết quả.

#### [NEW] `core/glossary_manager.py`
- Quản lý cơ sở dữ liệu `glossary` (SQLite/JSON).

- Quản lý việc **lưu và tải tiến trình dịch** (Save/Load Progress) để đối phó với lỗi API Limit và cho phép Human Review ngắt quãng.
- **Batch Processing**: Luồng dịch chính gom nhóm câu theo độ dài ký tự (`max_chars_per_batch`) để tăng tốc độ.
- Hàm `save_progress(docx_path, domain, translated_dict)`: Lưu bản nháp dưới dạng file `.json` tại thư mục `data/progress/` (sử dụng hash đường dẫn file chuẩn hóa).
- Hàm `load_progress(docx_path)`: Phục hồi lại dữ liệu đang làm dở.

## 4. Verification Plan (Kế hoạch Kiểm thử)
- [ ] **Test UI:** Giao diện hiển thị đúng 2 màn hình, thay đổi Dark/Light mode hoạt động. Bảng Glossary cho phép thêm/sửa/xóa thành công.
- [ ] **Test Docx:** Nạp file Word có format phức tạp (in đậm, bảng, hình). Kiểm tra xem file xuất ra có giữ nguyên 100% format hay không.
- [ ] **Test AI Pipeline:** 
  - AI nhận diện đúng lĩnh vực của đoạn test.
  - AI sử dụng đúng từ đã lưu trong Glossary.
  - Test trường hợp từ mới chưa có, AI tự dịch từ đó và lưu vào Glossary.
