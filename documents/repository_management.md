# Quản lý Repository & Quy trình Phát triển

Tài liệu này hướng dẫn các quy tắc và quy trình quản lý mã nguồn trên GitHub cho dự án **Translator Desktop App**.

## 1. Chiến lược phân nhánh (Branching)

Dự án áp dụng mô hình **Feature Branching** đơn giản:

- **`main`**: Nhánh chính, luôn ở trạng thái ổn định và có thể đóng gói (.exe) bất cứ lúc nào.
- **`develop`**: Nhánh tích hợp. Mọi tính năng mới sẽ được gộp vào đây trước khi đưa lên `main`.
- **`feature/`**: Các nhánh tính năng (Ví dụ: `feature/ai-engine`, `feature/ui-ux`).
- **`fix/`**: Các nhánh sửa lỗi khẩn cấp (Ví dụ: `fix/docx-encoding`).

**Quy trình:** Tạo nhánh mới -> Code & Test -> Pull Request vào `develop` -> Merge vào `main`.

## 2. Quy tắc Commit (Commit Messages)

Sử dụng chuẩn **Conventional Commits** để dễ dàng theo dõi lịch sử thay đổi:

Cấu trúc: `<type>: <description>`

- **feat**: Tính năng mới.
- **fix**: Sửa lỗi.
- **docs**: Cập nhật tài liệu (README, Wiki...).
- **style**: Thay đổi giao diện, định dạng code (không đổi logic).
- **refactor**: Tối ưu hóa code.
- **build**: Thay đổi hệ thống build, dependencies hoặc packaging.
- **test**: Thêm hoặc cập nhật unit tests.

*Ví dụ: `feat: tích hợp thêm model Claude 3.5 Sonnet`*

## 3. Bảo mật & Cấu hình (Security)

- **Tuyệt đối không commit**: API Key, mật khẩu, file `.env`, file `data/config.json`.
- **.gitignore**: Luôn cập nhật `.gitignore` khi thêm các loại file nháp hoặc file cấu hình mới.
- **Environment Templates**: Sử dụng `.env.example` để hướng dẫn người dùng cấu hình mà không làm lộ secret.

## 4. Quản lý Phiên bản & Phát hành (Releases)

- **Versioning**: Sử dụng Semantic Versioning (Ví dụ: `v1.0.0`).
- **GitHub Releases**: 
  - Không upload trực tiếp file `.exe` vào source code.
  - Sử dụng tính năng **Releases** của GitHub để đính kèm các bản build (`.exe`) tương ứng với từng phiên bản code.
  - Viết **Changelog** cho mỗi bản release để người dùng biết có gì mới.

## 5. Tự động hóa (CI/CD)

Trong tương lai, dự án hướng tới việc sử dụng **GitHub Actions** để:
1. Tự động kiểm tra lỗi code (Linting) mỗi khi push.
2. Tự động chạy Unit Test trong thư mục `test/`.
3. Tự động build file `.exe` khi tạo một Tag mới.

## 6. Lưu ý khi đóng gói (Packaging)

- Khi build file `.exe` bằng PyInstaller, đảm bảo cập nhật `BASE_DIR` trong mã nguồn để ứng dụng có thể lưu dữ liệu bền vững cạnh file thực thi.
- Tài liệu hướng dẫn cài đặt Pandoc phải luôn đi kèm với bản phân phối app.

---
*Tài liệu này được cập nhật lần cuối vào: 2026-04-26*
