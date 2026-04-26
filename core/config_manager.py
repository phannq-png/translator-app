import json
import os
import sys
from pathlib import Path

# Xác định thư mục gốc của ứng dụng (hỗ trợ đóng gói .exe)
if getattr(sys, 'frozen', False):
    # Nếu đang chạy từ file .exe
    BASE_DIR = Path(sys.executable).parent
else:
    # Nếu đang chạy từ mã nguồn python
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CONFIG_PATH = DATA_DIR / "config.json"

def get_default_config() -> dict:
    """Trả về cấu hình mặc định nếu chưa có."""
    return {
        "provider_detector": "Google Gemini",
        "detector_api_key": "",
        "model_detector": "gemini-1.5-flash",
        
        "provider_translator": "Google Gemini",
        "translator_api_key": "",
        "model_translator": "gemini-1.5-flash",
        
        "provider_reviewer": "Google Gemini",
        "reviewer_api_key": "",
        "model_reviewer": "gemini-1.5-pro",
        
        "max_chars_per_batch": 1000
    }

def load_config() -> dict:
    """Tải cấu hình từ config.json."""
    if not CONFIG_PATH.exists():
        save_config(get_default_config())
        return get_default_config()
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return get_default_config()

def save_config(config_data: dict) -> None:
    """Lưu cấu hình vào config.json."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4, ensure_ascii=False)
