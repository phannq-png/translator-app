import sqlite3
import os
import sys
import csv
from pathlib import Path

# Xác định thư mục gốc của ứng dụng (hỗ trợ đóng gói .exe)
if getattr(sys, 'frozen', False):
    # Nếu đang chạy từ file .exe
    BASE_DIR = Path(sys.executable).parent
else:
    # Nếu đang chạy từ mã nguồn python
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "glossary.db"

def _get_connection():
    """Tạo kết nối tới SQLite và khởi tạo bảng nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS glossary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            ja_term TEXT NOT NULL,
            vi_term TEXT NOT NULL,
            UNIQUE(domain, ja_term)
        )
    ''')
    conn.commit()
    return conn

def get_domains() -> list[str]:
    """Lấy danh sách các lĩnh vực hiện có."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT domain FROM glossary ORDER BY domain")
    domains = [row[0] for row in cursor.fetchall()]
    conn.close()
    return domains

def get_glossary(domain: str) -> dict[str, str]:
    """Lấy từ điển của một lĩnh vực cụ thể (dict {ja: vi})."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ja_term, vi_term FROM glossary WHERE domain=?", (domain,))
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def update_term(ja_term: str, vi_term: str, domain: str) -> None:
    """Thêm hoặc cập nhật thuật ngữ vào lĩnh vực tương ứng."""
    ja_term = ja_term.strip()
    vi_term = vi_term.strip()
    domain = domain.strip()
    
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO glossary (domain, ja_term, vi_term) 
        VALUES (?, ?, ?)
        ON CONFLICT(domain, ja_term) DO UPDATE SET vi_term=excluded.vi_term
    ''', (domain, ja_term, vi_term))
    conn.commit()
    conn.close()

def save_glossary_batch(domain: str, glossary_dict: dict[str, str]) -> None:
    """Lưu nhanh các thuật ngữ mới vào cơ sở dữ liệu, bỏ qua nếu đã tồn tại."""
    domain = domain.strip()
    conn = _get_connection()
    cursor = conn.cursor()
    for ja, vi in glossary_dict.items():
        ja = ja.strip()
        vi = vi.strip()
        # Sử dụng INSERT OR IGNORE để không ghi đè thuật ngữ cũ đã có
        cursor.execute('''
            INSERT OR IGNORE INTO glossary (domain, ja_term, vi_term) 
            VALUES (?, ?, ?)
        ''', (domain, ja, vi))
    conn.commit()
    conn.close()

def delete_term(ja_term: str, domain: str) -> None:
    """Xóa thuật ngữ khỏi cơ sở dữ liệu."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM glossary WHERE domain=? AND ja_term=?", (domain, ja_term))
    conn.commit()
    conn.close()

def export_glossary_to_csv(domain: str, file_path: str) -> bool:
    """Xuất thuật ngữ của một lĩnh vực (hoặc tất cả) ra file CSV."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        
        if domain == "ALL":
            cursor.execute("SELECT ja_term, vi_term, domain FROM glossary ORDER BY domain, ja_term")
            header = ["Tiếng Nhật", "Tiếng Việt", "Lĩnh vực"]
        else:
            cursor.execute("SELECT ja_term, vi_term FROM glossary WHERE domain=? ORDER BY ja_term", (domain,))
            header = ["Tiếng Nhật", "Tiếng Việt"]
            
        rows = cursor.fetchall()
        conn.close()
        
        with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        return True
    except Exception as e:
        print(f"Export Error: {e}")
        return False

def import_glossary_from_csv(domain: str, file_path: str) -> tuple[int, int]:
    """
    Nhập thuật ngữ từ file CSV.
    Trả về: (số từ thêm mới, số từ lỗi)
    """
    success_count = 0
    error_count = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            # Tự động nhận diện delimiter nếu có thể, mặc định dùng comma
            reader = csv.reader(f)
            header = next(reader, None)
            
            # Kiểm tra cấu trúc header để quyết định lấy domain từ đâu
            # Nếu file có 3 cột, ưu tiên cột 3 là domain
            has_domain_col = header and len(header) >= 3
            
            for row in reader:
                if len(row) < 2: 
                    error_count += 1
                    continue
                
                ja, vi = row[0].strip(), row[1].strip()
                if not ja or not vi:
                    error_count += 1
                    continue
                
                # Xác định domain
                current_domain = domain
                if has_domain_col and len(row) >= 3:
                    current_domain = row[2].strip() or domain
                
                try:
                    update_term(ja, vi, current_domain)
                    success_count += 1
                except:
                    error_count += 1
                    
        return success_count, error_count
    except Exception as e:
        print(f"Import Error: {e}")
        return 0, -1
