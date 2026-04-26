# Entry point cho ứng dụng Translator Desktop App
import os
import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv

# Import các giao diện
from ui.ui_main import MainView
from ui.ui_glossary import GlossaryWindow
from ui.ui_settings import SettingsWindow
from core.progress_manager import get_recent_progress, delete_progress_by_file
from datetime import datetime

# Load biến môi trường từ file .env (nếu có)
load_dotenv()

# Cấu hình giao diện mặc định
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("AI Translator Desktop App")
        # Khởi chạy full màn hình (Maximized)
        self.after(0, lambda: self.state('zoomed'))
        
        # Tạo Menu / Sidebar bên trái
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Translator App", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 30))
        
        self.btn_settings = ctk.CTkButton(self.sidebar_frame, text="⚙️ Cài đặt AI & API", command=self.open_settings)
        self.btn_settings.pack(padx=20, pady=10)
        
        self.btn_glossary = ctk.CTkButton(self.sidebar_frame, text="📚 Quản lý Thuật ngữ", command=self.open_glossary)
        self.btn_glossary.pack(padx=20, pady=10)
        
        # Vùng hiển thị chính bên phải
        self.main_view = MainView(self)
        self.main_view.pack(side="right", fill="both", expand=True)
        
        # Thêm mục Progress gần đây vào Sidebar
        self.lbl_recent = ctk.CTkLabel(self.sidebar_frame, text="🕒 Tiến trình gần đây", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_recent.pack(padx=20, pady=(30, 5), anchor="w")
        
        self.recent_frame = ctk.CTkScrollableFrame(self.sidebar_frame, width=180, height=300, fg_color="transparent")
        self.recent_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.update_recent_sidebar()
        
        self.glossary_window = None
        self.settings_window = None

    def open_glossary(self):
        if self.glossary_window is None or not self.glossary_window.winfo_exists():
            self.glossary_window = GlossaryWindow(self)
        else:
            self.glossary_window.focus()
            
    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus()

    def update_recent_sidebar(self):
        """Cập nhật danh sách file gần đây ở sidebar."""
        for child in self.recent_frame.winfo_children():
            child.destroy()
            
        recent_files = get_recent_progress()
        if not recent_files:
            lbl = ctk.CTkLabel(self.recent_frame, text="Chưa có file nào", font=("Arial", 10, "italic"), text_color="gray")
            lbl.pack(pady=10)
            return
            
        for item in recent_files[:10]: # Lấy 10 file gần nhất
            path = item['docx_path']
            filename = os.path.basename(path)
            count = item['count']
            last_updated = item['last_updated']
            
            # Định dạng ngày giờ
            time_str = datetime.fromtimestamp(last_updated).strftime("%d/%m %H:%M")
            
            row = ctk.CTkFrame(self.recent_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            # Button cho từng file
            btn_text = f"{filename}\n{time_str} • {count} đoạn"
            btn = ctk.CTkButton(row, text=btn_text, font=("Arial", 10), 
                                fg_color="transparent", text_color=("black", "white"),
                                anchor="w", height=45,
                                hover_color=("gray85", "gray25"),
                                command=lambda p=path: self.load_recent_file(p))
            btn.pack(side="left", fill="x", expand=True)
            
            # Nút xóa tiến trình
            json_path = item['json_path']
            btn_del = ctk.CTkButton(row, text="×", width=20, height=20, 
                                    fg_color="transparent", text_color="gray", 
                                    hover_color=("gray75", "gray35"),
                                    command=lambda p=path, j=json_path: self.confirm_delete_progress(p, j))
            btn_del.pack(side="right", padx=2)

    def confirm_delete_progress(self, docx_path, json_path):
        if messagebox.askyesno("Xác nhận", f"Xóa tiến trình của file:\n{os.path.basename(docx_path)}?"):
            if delete_progress_by_file(json_path):
                self.update_recent_sidebar()
            else:
                messagebox.showerror("Lỗi", "Không thể xóa file tiến trình.")

    def load_recent_file(self, path):
        if os.path.exists(path):
            self.main_view.load_file_direct(path)
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy file:\n{path}")
            # Có thể xóa khỏi list nếu muốn, nhưng ở đây cứ để đó

def main():
    print("Khởi chạy ứng dụng Translator...")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
