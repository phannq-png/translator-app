import json
import os
import hashlib
import time

PROGRESS_DIR = "data/progress"

def _get_progress_path(docx_path: str) -> str:
    """Tạo đường dẫn file json dựa trên hash của đường dẫn file docx."""
    if not os.path.exists(PROGRESS_DIR):
        os.makedirs(PROGRESS_DIR)
    
    # Chuẩn hóa đường dẫn để tránh lỗi khác nhau giữa hoa/thường trên Windows
    normalized_path = os.path.abspath(docx_path).lower()
    file_hash = hashlib.md5(normalized_path.encode('utf-8')).hexdigest()
    return os.path.join(PROGRESS_DIR, f"{file_hash}.json")

def save_progress(docx_path: str, domain: str, translated_dict: dict):
    """Lưu tiến trình dịch vào file JSON."""
    docx_path = os.path.abspath(docx_path)
    progress_file = _get_progress_path(docx_path)
    data = {
        "docx_path": docx_path,
        "domain": domain,
        "translations": translated_dict,
        "last_updated": time.time()
    }
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_progress(docx_path: str) -> dict:
    """Tải tiến trình dịch nếu tồn tại."""
    docx_path = os.path.abspath(docx_path)
    progress_file = _get_progress_path(docx_path)
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    return None

def get_recent_progress() -> list:
    """Lấy danh sách các file đã có tiến trình lưu lại."""
    if not os.path.exists(PROGRESS_DIR):
        return []
    
    recent = []
    for filename in os.listdir(PROGRESS_DIR):
        if filename.endswith(".json"):
            path = os.path.join(PROGRESS_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    recent.append({
                        "docx_path": data.get("docx_path", "Unknown"),
                        "json_path": path,
                        "domain": data.get("domain", ""),
                        "last_updated": data.get("last_updated", 0),
                        "count": len(data.get("translations", {}))
                    })
            except:
                continue
                
    # Sắp xếp theo thời gian mới nhất
    recent.sort(key=lambda x: x['last_updated'], reverse=True)
    return recent

def delete_progress(docx_path: str) -> bool:
    """Xóa file tiến trình của một tài liệu dựa trên docx_path."""
    docx_path = os.path.abspath(docx_path)
    progress_file = _get_progress_path(docx_path)
    if os.path.exists(progress_file):
        try:
            os.remove(progress_file)
            return True
        except:
            return False
    return False

def delete_progress_by_file(json_path: str) -> bool:
    """Xóa file tiến trình bằng đường dẫn trực tiếp tới file JSON."""
    if os.path.exists(json_path):
        try:
            os.remove(json_path)
            return True
        except:
            return False
    return False
