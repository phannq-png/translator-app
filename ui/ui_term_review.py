import customtkinter as ctk
from core.glossary_manager import get_glossary, update_term, delete_term, get_domains
from tkinter import messagebox

class TermReviewWindow(ctk.CTkToplevel):
    def __init__(self, master, domain, chunks, start_translation_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Kiểm duyệt thuật ngữ trước khi dịch")
        self.geometry("800x600")
        self.attributes("-topmost", True)
        
        self.domain = domain
        self.chunks = chunks
        self.start_translation_callback = start_translation_callback
        
        # Header
        self.lbl_title = ctk.CTkLabel(self, text=f"Review thuật ngữ - Lĩnh vực: {domain}", font=("Arial", 16, "bold"))
        self.lbl_title.pack(pady=10)
        
        self.lbl_info = ctk.CTkLabel(self, text="Hệ thống đã trích xuất các thuật ngữ dưới đây. Vui lòng kiểm tra và sửa lại nếu cần.", text_color=("#D35400", "#E67E22"))
        self.lbl_info.pack(pady=5)
        
        # Scrollable area for terms
        self.scroll_terms = ctk.CTkScrollableFrame(self, label_text="Danh sách thuật ngữ trong tài liệu")
        self.scroll_terms.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Bottom area for manual add and OK button
        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_bottom.pack(fill="x", padx=20, pady=20)
        
        # Manual Add
        self.frame_add = ctk.CTkFrame(self.frame_bottom, fg_color="transparent")
        self.frame_add.pack(side="left", fill="x", expand=True)
        
        self.ent_ja = ctk.CTkEntry(self.frame_add, placeholder_text="Thêm Tiếng Nhật...", width=150)
        self.ent_ja.pack(side="left", padx=5)
        
        self.ent_vi = ctk.CTkEntry(self.frame_add, placeholder_text="Thêm Tiếng Việt...", width=150)
        self.ent_vi.pack(side="left", padx=5)
        
        self.btn_add = ctk.CTkButton(self.frame_add, text="+", width=40, command=self.add_term)
        self.btn_add.pack(side="left", padx=5)
        
        # OK Button
        self.btn_confirm = ctk.CTkButton(self.frame_bottom, text="Xác nhận & Bắt đầu Dịch", 
                                        fg_color="green", font=("Arial", 14, "bold"),
                                        height=40, command=self.confirm_and_start)
        self.btn_confirm.pack(side="right", padx=10)
        
        self.load_terms()
        
    def load_terms(self):
        for child in self.scroll_terms.winfo_children():
            child.destroy()
            
        sample_text = ""
        for chunk in self.chunks[:5]: 
            sample_text += chunk['text'] + "\n"
            
        all_glossary = get_glossary(self.domain)
        active_terms = {ja: vi for ja, vi in all_glossary.items() if ja in sample_text}
        
        if not active_terms:
            lbl = ctk.CTkLabel(self.scroll_terms, text="Không tìm thấy thuật ngữ nào. Bạn có thể thêm thủ công hoặc tiếp tục.", text_color="gray")
            lbl.pack(pady=50)
            return

        for ja, vi in active_terms.items():
            row = ctk.CTkFrame(self.scroll_terms, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            lbl_ja = ctk.CTkLabel(row, text=ja, font=("Arial", 12, "bold"), width=250, anchor="w")
            lbl_ja.pack(side="left", padx=10)
            
            ent_vi = ctk.CTkEntry(row, width=250)
            ent_vi.insert(0, vi)
            ent_vi.pack(side="left", padx=10)
            
            # Save individual term when entry focus out or on Enter could be added, 
            # but for simplicity we'll add a small save icon or just save all at once.
            btn_save = ctk.CTkButton(row, text="Lưu", width=50, 
                                     command=lambda j=ja, e=ent_vi: self.quick_save(j, e.get()))
            btn_save.pack(side="left", padx=5)
            
            btn_del = ctk.CTkButton(row, text="🗑️", width=40, fg_color="red",
                                    command=lambda j=ja: self.quick_delete(j))
            btn_del.pack(side="right", padx=10)

    def quick_save(self, ja, vi):
        update_term(ja, vi, self.domain)
        # messagebox.showinfo("OK", f"Đã cập nhật '{ja}'")

    def quick_delete(self, ja):
        if messagebox.askyesno("Xóa", f"Xóa '{ja}'?"):
            delete_term(ja, self.domain)
            self.load_terms()

    def add_term(self):
        ja = self.ent_ja.get().strip()
        vi = self.ent_vi.get().strip()
        if ja and vi:
            update_term(ja, vi, self.domain)
            self.ent_ja.delete(0, "end")
            self.ent_vi.delete(0, "end")
            self.load_terms()

    def confirm_and_start(self):
        # Close this window
        self.destroy()
        # Trigger the translation in main window
        self.start_translation_callback()
