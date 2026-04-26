from google import genai
import json
import os

# Tải config để lấy API Key của bạn
config_path = "data/config.json"

if not os.path.exists(config_path):
    print("Không tìm thấy file data/config.json. Vui lòng mở App và lưu cài đặt API Key trước.")
else:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Thử lấy key từ bộ Translator (hoặc Detector/Reviewer)
    api_key = config.get("translator_api_key") or config.get("detector_api_key") or config.get("reviewer_api_key")

    if not api_key:
        print("Bạn chưa nhập API Key trong phần Cài đặt của App!")
    else:
        try:
            print(f"Đang kiểm tra API Key: {api_key[:10]}...")
            client = genai.Client(api_key=api_key)
            print("\n--- DANH SÁCH MODEL KHẢ DỤNG CHO API KEY NÀY ---")
            found = False
            for m in client.models.list():
                # API mới dùng supported_actions, API cũ dùng supported_methods
                methods = getattr(m, 'supported_actions', None) or getattr(m, 'supported_methods', [])
                if "generateContent" in methods:
                    # Loại bỏ tiền tố 'models/' để copy vào App cho tiện
                    name = m.name or ""
                    clean_name = name.replace("models/", "")
                    print(f"- {clean_name}")
                    found = True
            
            if not found:
                print("Không tìm thấy model nào hỗ trợ generateContent.")
                
            print("\n-----------------------------------------------")
            print("HƯỚNG DẪN: Bạn hãy copy chính xác tên model ở trên (ví dụ: gemini-1.5-flash-latest)")
            print("vào ô 'Tên Model' trong phần Cài đặt của ứng dụng.")
            
        except Exception as e:
            print(f"\n[LỖI] Không thể kết nối tới Google API: {e}")
            print("Vui lòng kiểm tra lại API Key hoặc kết nối mạng.")
