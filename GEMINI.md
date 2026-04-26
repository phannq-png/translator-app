# Hướng dẫn cho AI Agent (Antigravity)

Đây là bộ quy tắc bắt buộc mà AI phải tuân thủ khi làm việc với dự án **Translator Desktop App**. Đọc và áp dụng TRƯỚC KHI thực hiện bất kỳ thay đổi nào.

---

## 1. Quy trình Git (BẮT BUỘC)

Mọi thay đổi code phải đi kèm với một commit Git đúng chuẩn sau khi hoàn thành.

**Lệnh commit chuẩn:**
```powershell
& "C:\Program Files\Git\cmd\git.exe" add .
& "C:\Program Files\Git\cmd\git.exe" commit -m "<type>: <mô tả ngắn gọn bằng tiếng Việt>"
& "C:\Program Files\Git\cmd\git.exe" push origin main
```

**Các loại commit hợp lệ (`<type>`):**
- `feat`: Thêm tính năng mới.
- `fix`: Sửa lỗi.
- `docs`: Cập nhật tài liệu, README.
- `style`: Thay đổi giao diện, không đổi logic.
- `refactor`: Tối ưu code, không đổi tính năng.
- `build`: Thay đổi liên quan đến build (.exe) hoặc dependencies.
- `test`: Thêm hoặc cập nhật Unit Test.

**Ví dụ commit hợp lệ:**
```
feat: thêm tính năng xuất file PDF
fix: sửa lỗi lệch index khi tái tạo docx
docs: cập nhật hướng dẫn cài đặt Pandoc
```

---

## 2. Bảo mật (TUYỆT ĐỐI KHÔNG VI PHẠM)

- **KHÔNG BAO GIỜ** commit các file sau: `.env`, `data/config.json`, `data/glossary.db`, `data/output/`, bất kỳ file nào chứa API Key.
- Khi tạo file cấu hình mẫu, **chỉ** dùng `.env.example` với giá trị rỗng.
- Nếu phát hiện bất kỳ API Key hoặc thông tin nhạy cảm nào trong code → xóa ngay và thông báo cho người dùng.

---

## 3. Cấu trúc dự án & Quy ước code

- **Thư mục `core/`**: Chỉ chứa logic xử lý (không chứa UI).
- **Thư mục `ui/`**: Chỉ chứa mã nguồn giao diện CustomTkinter.
- **Thư mục `documents/`**: Mọi tài liệu, ghi chú, kế hoạch.
- **Thư mục `test/`**: Chỉ chứa file test, **không chứa** dữ liệu nhạy cảm.
- Mọi module trong `core/` xử lý đường dẫn file phải hỗ trợ cả môi trường chạy trực tiếp (Python) và đóng gói (.exe) bằng cách kiểm tra `sys.frozen`.

---

## 4. Tài liệu tham chiếu

Trước khi làm tính năng lớn, đọc các tài liệu sau:
- Quy trình chi tiết: `documents/workflow.md`
- Kế hoạch tổng thể: `documents/implementation_plan.md`
- Quy tắc code: `documents/coding_rules.md`
- Quy trình quản lý repository: `documents/repository_management.md`
