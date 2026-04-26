# Cấu trúc Thư mục Dự kiến (Project Structure)

Dưới đây là cấu trúc thư mục tiêu chuẩn dự kiến cho dự án **Translator Desktop App**, được thiết kế theo mô hình phân tách rõ ràng giữa Giao diện (UI) và Logic Xử lý (Core) để dễ dàng bảo trì và mở rộng.

```text
Translator/
│
├── main.py                     # Entry point: Khởi chạy ứng dụng và nạp giao diện
├── requirements.txt            # Danh sách các thư viện cần cài đặt (pip install -r ...)
├── .env                        # Chứa biến môi trường (Ví dụ: GEMINI_API_KEY)
├── .gitignore                  # Bỏ qua các file không đưa lên Git (.env, data, v.venv...)
│
├── documents/                  # Thư mục chứa tài liệu mô tả dự án (dành cho developer)
│   ├── README.md               # Tổng quan dự án
│   ├── workflow.md             # Luồng công việc 
│   ├── requirements.md         # Yêu cầu nghiệp vụ chi tiết
│   ├── technical_setup.md      # Hướng dẫn setup môi trường
│   └── project_structure.md    # File cấu trúc này
│
├── core/                       # Thư mục chứa Logic xử lý chính (Backend)
│   ├── __init__.py
│   ├── docx_processor.py       # Chịu trách nhiệm bóc tách (extract) và ghi đè (reconstruct) file .docx
│   ├── ai_engine.py            # Chịu trách nhiệm kết nối Google API: Nhận diện lĩnh vực, Dịch, Review
│   ├── glossary_manager.py     # Chịu trách nhiệm thêm/sửa/xóa và load bộ Glossary từ Database
│   └── config_manager.py       # Quản lý Import/Export và Load cấu hình API Key đa AI
│
├── ui/                         # Thư mục chứa Giao diện người dùng (Frontend - CustomTkinter)
│   ├── __init__.py
│   ├── ui_main.py              # Xây dựng các component cho Màn hình chính (Khu vực dịch)
│   ├── ui_glossary.py          # Xây dựng Cửa sổ/Màn hình phụ chuyên quản lý thuật ngữ
│   └── ui_settings.py          # Màn hình cài đặt cấu hình Đa AI và API Key
│
└── data/                       # Thư mục chứa dữ liệu sinh ra trong quá trình chạy (Local DB)
    ├── glossary.db             # Database SQLite chứa toàn bộ thuật ngữ phân chia theo lĩnh vực
    ├── config.json             # File lưu API Keys và thiết lập của các AI
    └── output/                 # Thư mục mặc định để chứa các file Word đã dịch xong (tùy chọn)
```

### Giải thích nguyên lý hoạt động theo cấu trúc này:
1. Khi chạy lệnh `python main.py`, file này sẽ gọi module từ thư mục `/ui` để vẽ lên màn hình giao diện.
2. Khi người dùng nạp file Word và bấm "Dịch", giao diện ở `/ui` sẽ gửi tín hiệu xuống thư mục `/core`.
3. Trong `/core`:
   - `docx_processor.py` đọc file.
   - `config_manager.py` sẽ lấy đúng API Key từ `config.json` tùy theo loại AI đang cần chạy.
   - `ai_engine.py` gọi tới AI (dựa trên cấu hình tương ứng) để phân tích và dịch.
   - `glossary_manager.py` sẽ chọc vào database ở thư mục `/data/glossary.db` để lấy đúng từ điển cung cấp cho AI.
4. Sau khi có kết quả, dữ liệu đẩy ngược lên hiển thị trên màn hình để người dùng Review.
