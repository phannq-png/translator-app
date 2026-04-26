import customtkinter as ctk
from core.glossary_manager import (
    get_domains, get_glossary, update_term, delete_term, 
    export_glossary_to_csv, import_glossary_from_csv
)
from tkinter import messagebox, filedialog

class GlossaryWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Quản lý Thuật ngữ (Glossary)")
        self.geometry("700x550")
        self.attributes("-topmost", True)
        
        self.current_domain = None
        
        # Lĩnh vực (Domain) Selector
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(fill="x", padx=10, pady=10)
        
        self.lbl_domain = ctk.CTkLabel(self.frame_top, text="Lĩnh vực:")
        self.lbl_domain.pack(side="left", padx=5)
        
        domains = get_domains()
        self.cb_domain = ctk.CTkComboBox(self.frame_top, values=domains, command=self.load_terms)
        self.cb_domain.pack(side="left", padx=5, fill="x", expand=True)
        
        self.btn_import = ctk.CTkButton(self.frame_top, text="📥 Nhập", width=70, command=self.import_csv)
        self.btn_import.pack(side="right", padx=2)
        
        self.btn_export = ctk.CTkButton(self.frame_top, text="📤 Xuất", width=70, command=self.export_csv)
        self.btn_export.pack(side="right", padx=2)
        
        # Bảng hiển thị (Scrollable Frame)
        self.scroll_terms = ctk.CTkScrollableFrame(self, label_text="Danh sách thuật ngữ")
        self.scroll_terms.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Thêm/Sửa từ
        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_bottom.pack(fill="x", padx=10, pady=10)
        
        self.ent_ja = ctk.CTkEntry(self.frame_bottom, placeholder_text="Tiếng Nhật")
        self.ent_ja.pack(side="left", padx=5, expand=True, fill="x")
        
        self.ent_vi = ctk.CTkEntry(self.frame_bottom, placeholder_text="Tiếng Việt")
        self.ent_vi.pack(side="left", padx=5, expand=True, fill="x")
        
        self.btn_save = ctk.CTkButton(self.frame_bottom, text="Lưu/Sửa", command=self.save_term, fg_color="green")
        self.btn_save.pack(side="left", padx=5)
        
        if self.cb_domain.get():
            self.load_terms(self.cb_domain.get())
            
    def load_terms(self, domain):
        self.current_domain = domain
        # Xóa các hàng cũ
        for child in self.scroll_terms.winfo_children():
            child.destroy()
            
        glossary = get_glossary(domain)
        for i, (ja, vi) in enumerate(glossary.items()):
            row = ctk.CTkFrame(self.scroll_terms, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            lbl_ja = ctk.CTkLabel(row, text=ja, width=200, anchor="w")
            lbl_ja.pack(side="left", padx=5)
            
            lbl_arrow = ctk.CTkLabel(row, text="➔", width=30)
            lbl_arrow.pack(side="left")
            
            lbl_vi = ctk.CTkLabel(row, text=vi, width=200, anchor="w", text_color=("#1F6AA5", "#3B8ED0"))
            lbl_vi.pack(side="left", padx=5)
            
            # Nút sửa (đưa lên entry)
            btn_edit = ctk.CTkButton(row, text="✏️", width=30, fg_color="gray", 
                                     command=lambda j=ja, v=vi: self.prepare_edit(j, v))
            btn_edit.pack(side="right", padx=2)
            
            # Nút xóa
            btn_del = ctk.CTkButton(row, text="🗑️", width=30, fg_color="red", 
                                    command=lambda j=ja: self.delete_term_ui(j))
            btn_del.pack(side="right", padx=2)
            
    def prepare_edit(self, ja, vi):
        self.ent_ja.delete(0, "end")
        self.ent_ja.insert(0, ja)
        self.ent_vi.delete(0, "end")
        self.ent_vi.insert(0, vi)
        
    def delete_term_ui(self, ja):
        if messagebox.askyesno("Xác nhận", f"Xóa thuật ngữ '{ja}'?"):
            delete_term(ja, self.current_domain)
            self.load_terms(self.current_domain)
            
    def save_term(self):
        domain = self.cb_domain.get().strip()
        ja = self.ent_ja.get().strip()
        vi = self.ent_vi.get().strip()
        
        if domain and ja and vi:
            update_term(ja, vi, domain)
            self.ent_ja.delete(0, "end")
            self.ent_vi.delete(0, "end")
            self.load_terms(domain)
            self.cb_domain.configure(values=get_domains())

    def export_csv(self):
        domain = self.cb_domain.get()
        if not domain:
            # Nếu không chọn domain nào, hỏi xem có muốn xuất tất cả không
            if messagebox.askyesno("Xuất dữ liệu", "Bạn chưa chọn lĩnh vực. Xuất TOÀN BỘ thuật ngữ?"):
                domain = "ALL"
            else:
                return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"glossary_{domain.lower()}.csv"
        )
        if file_path:
            if export_glossary_to_csv(domain, file_path):
                messagebox.showinfo("Thành công", f"Đã xuất dữ liệu thuật ngữ!")
            else:
                messagebox.showerror("Lỗi", "Không thể xuất file.")

    def import_csv(self):
        domain = self.cb_domain.get()
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            success, errors = import_glossary_from_csv(domain, file_path)
            if errors == -1:
                messagebox.showerror("Lỗi", "Có lỗi xảy ra khi đọc file.")
            else:
                messagebox.showinfo("Hoàn tất", f"Đã nhập thành công {success} thuật ngữ.\nSố dòng lỗi: {errors}")
                if domain:
                    self.load_terms(domain)
                self.cb_domain.configure(values=get_domains())
