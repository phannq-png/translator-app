import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.config_manager import load_config, save_config

PROVIDERS = ["Google Gemini", "OpenAI", "Anthropic"]

POPULAR_MODELS = {
    "Google Gemini": [
        "gemini-3-flash",
        "gemini-3-flash-lite",
        "gemini-3-pro",
        "gemini-2.5-flash", 
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.0-pro-exp",
        "gemini-1.5-flash", 
        "gemini-1.5-flash-8b", 
        "gemini-1.5-pro", 
        "gemini-1.0-pro"
    ],
    "OpenAI": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    "Anthropic": ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"]
}

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Cài đặt AI & API Keys")
        self.geometry("550x750")
        self.attributes("-topmost", True)
        
        self.config_data = load_config()
        
        # Scrollable frame for settings
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_title = ctk.CTkLabel(self.scroll_frame, text="Cấu hình API Key Đa AI", font=("Arial", 16, "bold"))
        self.lbl_title.pack(pady=10)
        
        # --- DETECTOR SETTINGS ---
        self.frame_det = ctk.CTkFrame(self.scroll_frame)
        self.frame_det.pack(fill="x", padx=20, pady=5)
        
        self.lbl_det_title = ctk.CTkLabel(self.frame_det, text="🔍 AI Nhận diện Lĩnh vực", font=("Arial", 13, "bold"))
        self.lbl_det_title.pack(anchor="w", padx=10, pady=(5,0))
        
        self.cb_prov_det = ctk.CTkComboBox(self.frame_det, values=PROVIDERS, width=200, command=self.update_models_det)
        self.cb_prov_det.pack(anchor="w", padx=10, pady=5)
        current_prov_det = self.config_data.get("provider_detector", "Google Gemini")
        self.cb_prov_det.set(current_prov_det)
        
        self.ent_det_key = ctk.CTkEntry(self.frame_det, placeholder_text="API Key Nhận diện")
        self.ent_det_key.pack(fill="x", padx=10, pady=2)
        self.ent_det_key.insert(0, self.config_data.get("detector_api_key", ""))
        
        self.lbl_model_det = ctk.CTkLabel(self.frame_det, text="Tên Model (Nên dùng model rẻ nhất):", text_color="gray")
        self.lbl_model_det.pack(anchor="w", padx=10)
        
        self.cb_model_det = ctk.CTkComboBox(self.frame_det, values=POPULAR_MODELS.get(current_prov_det, []))
        self.cb_model_det.pack(fill="x", padx=10, pady=(0, 10))
        self.cb_model_det.set(self.config_data.get("model_detector", "gemini-1.5-flash"))
        
        # --- TRANSLATOR SETTINGS ---
        self.frame_trans = ctk.CTkFrame(self.scroll_frame)
        self.frame_trans.pack(fill="x", padx=20, pady=5)
        
        self.lbl_trans_title = ctk.CTkLabel(self.frame_trans, text="🤖 AI Dịch thuật", font=("Arial", 13, "bold"))
        self.lbl_trans_title.pack(anchor="w", padx=10, pady=(5,0))
        
        self.cb_prov_trans = ctk.CTkComboBox(self.frame_trans, values=PROVIDERS, width=200, command=self.update_models_trans)
        self.cb_prov_trans.pack(anchor="w", padx=10, pady=5)
        current_prov_trans = self.config_data.get("provider_translator", "Google Gemini")
        self.cb_prov_trans.set(current_prov_trans)
        
        self.ent_trans_key = ctk.CTkEntry(self.frame_trans, placeholder_text="API Key Dịch")
        self.ent_trans_key.pack(fill="x", padx=10, pady=2)
        self.ent_trans_key.insert(0, self.config_data.get("translator_api_key", ""))
        
        self.lbl_model_trans = ctk.CTkLabel(self.frame_trans, text="Tên Model (Model chất lượng trung bình):", text_color="gray")
        self.lbl_model_trans.pack(anchor="w", padx=10)
        
        self.cb_model_trans = ctk.CTkComboBox(self.frame_trans, values=POPULAR_MODELS.get(current_prov_trans, []))
        self.cb_model_trans.pack(fill="x", padx=10, pady=(0, 10))
        self.cb_model_trans.set(self.config_data.get("model_translator", "gemini-1.5-flash"))
        
        # --- REVIEWER SETTINGS ---
        self.frame_rev = ctk.CTkFrame(self.scroll_frame)
        self.frame_rev.pack(fill="x", padx=20, pady=5)
        
        self.lbl_rev_title = ctk.CTkLabel(self.frame_rev, text="🧐 AI Kiểm duyệt (Reviewer)", font=("Arial", 13, "bold"))
        self.lbl_rev_title.pack(anchor="w", padx=10, pady=(5,0))
        
        self.cb_prov_rev = ctk.CTkComboBox(self.frame_rev, values=PROVIDERS, width=200, command=self.update_models_rev)
        self.cb_prov_rev.pack(anchor="w", padx=10, pady=5)
        current_prov_rev = self.config_data.get("provider_reviewer", "Google Gemini")
        self.cb_prov_rev.set(current_prov_rev)
        
        self.ent_rev_key = ctk.CTkEntry(self.frame_rev, placeholder_text="API Key Review")
        self.ent_rev_key.pack(fill="x", padx=10, pady=2)
        self.ent_rev_key.insert(0, self.config_data.get("reviewer_api_key", ""))
        
        self.lbl_model_rev = ctk.CTkLabel(self.frame_rev, text="Tên Model (Nên dùng model tốt nhất):", text_color="gray")
        self.lbl_model_rev.pack(anchor="w", padx=10)
        
        self.cb_model_rev = ctk.CTkComboBox(self.frame_rev, values=POPULAR_MODELS.get(current_prov_rev, []))
        self.cb_model_rev.pack(fill="x", padx=10, pady=(0, 10))
        self.cb_model_rev.set(self.config_data.get("model_reviewer", "gemini-1.5-pro"))
                # --- BATCH SIZE SETTINGS ---
        self.frame_batch = ctk.CTkFrame(self.scroll_frame)
        self.frame_batch.pack(fill="x", padx=20, pady=5)
        
        self.lbl_batch = ctk.CTkLabel(self.frame_batch, text="📦 Số đoạn văn mỗi khối (Batch Size):", font=("Arial", 13, "bold"))
        self.lbl_batch.pack(side="left", padx=10, pady=10)
        
        self.ent_batch = ctk.CTkEntry(self.frame_batch, width=80)
        self.ent_batch.pack(side="left", padx=10)
        self.ent_batch.insert(0, str(self.config_data.get("batch_size", 5)))
        
        # --- BOTTOM ACTION AREA ---
        self.frame_bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom.pack(side="bottom", fill="x", padx=20, pady=20)
        
        # Row 1: Export/Import
        self.frame_io = ctk.CTkFrame(self.frame_bottom, fg_color="transparent")
        self.frame_io.pack(fill="x", pady=(0, 10))
        
        self.btn_export = ctk.CTkButton(self.frame_io, text="📤 Xuất JSON", 
                                       fg_color="gray", hover_color="gray25",
                                       command=self.export_config)
        self.btn_export.pack(side="left", padx=5, expand=True, fill="x")
        
        self.btn_import = ctk.CTkButton(self.frame_io, text="📥 Nhập JSON", 
                                       fg_color="gray", hover_color="gray25",
                                       command=self.import_config)
        self.btn_import.pack(side="left", padx=5, expand=True, fill="x")
        
        # Row 2: Save
        self.btn_save = ctk.CTkButton(self.frame_bottom, text="💾 Lưu Cấu hình & Áp dụng", 
                                     height=40, font=("Arial", 14, "bold"),
                                     command=self.save_settings)
        self.btn_save.pack(fill="x", padx=5)

    def update_models_det(self, choice):
        self.cb_model_det.configure(values=POPULAR_MODELS.get(choice, []))
        if POPULAR_MODELS.get(choice):
            self.cb_model_det.set(POPULAR_MODELS[choice][0])
        else:
            self.cb_model_det.set("")

    def update_models_trans(self, choice):
        self.cb_model_trans.configure(values=POPULAR_MODELS.get(choice, []))
        if POPULAR_MODELS.get(choice):
            self.cb_model_trans.set(POPULAR_MODELS[choice][0])
        else:
            self.cb_model_trans.set("")
            
    def update_models_rev(self, choice):
        self.cb_model_rev.configure(values=POPULAR_MODELS.get(choice, []))
        if POPULAR_MODELS.get(choice):
            self.cb_model_rev.set(POPULAR_MODELS[choice][0])
        else:
            self.cb_model_rev.set("")
        
    def save_settings(self):
        try:
            self.config_data["batch_size"] = int(self.ent_batch.get())
        except:
            self.config_data["batch_size"] = 5
            
        self.config_data["provider_detector"] = self.cb_prov_det.get().strip()
        self.config_data["detector_api_key"] = self.ent_det_key.get().strip()
        self.config_data["model_detector"] = self.cb_model_det.get().strip()

        self.config_data["provider_translator"] = self.cb_prov_trans.get().strip()
        self.config_data["translator_api_key"] = self.ent_trans_key.get().strip()
        self.config_data["model_translator"] = self.cb_model_trans.get().strip()
        
        self.config_data["provider_reviewer"] = self.cb_prov_rev.get().strip()
        self.config_data["reviewer_api_key"] = self.ent_rev_key.get().strip()
        self.config_data["model_reviewer"] = self.cb_model_rev.get().strip()
        
        save_config(self.config_data)
        self.destroy()

    def export_config(self):
        """Xuất cấu hình ra file JSON."""
        # Tổng hợp dữ liệu hiện tại từ UI trước khi xuất
        current_config = self._get_current_ui_config()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile="ai_config.json"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(current_config, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Thành công", f"Đã xuất cấu hình ra:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file: {e}")

    def import_config(self):
        """Nhập cấu hình từ file JSON."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    new_config = json.load(f)
                
                # Cập nhật UI từ dữ liệu mới
                self.config_data = new_config
                self._load_config_to_ui()
                messagebox.showinfo("Thành công", "Đã nhập cấu hình mới. Hãy nhấn 'Lưu Cấu hình' để áp dụng.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể nhập file: {e}")

    def _get_current_ui_config(self) -> dict:
        """Lấy dữ liệu từ các widget trên UI."""
        config: dict = {}
        try: config["batch_size"] = int(self.ent_batch.get())
        except: config["batch_size"] = 5
        
        config["provider_detector"] = self.cb_prov_det.get().strip()
        config["detector_api_key"] = self.ent_det_key.get().strip()
        config["model_detector"] = self.cb_model_det.get().strip()

        config["provider_translator"] = self.cb_prov_trans.get().strip()
        config["translator_api_key"] = self.ent_trans_key.get().strip()
        config["model_translator"] = self.cb_model_trans.get().strip()
        
        config["provider_reviewer"] = self.cb_prov_rev.get().strip()
        config["reviewer_api_key"] = self.ent_rev_key.get().strip()
        config["model_reviewer"] = self.cb_model_rev.get().strip()
        return config

    def _load_config_to_ui(self):
        """Đổ dữ liệu từ self.config_data vào các widget UI."""
        self.cb_prov_det.set(self.config_data.get("provider_detector", "Google Gemini"))
        self.ent_det_key.delete(0, "end")
        self.ent_det_key.insert(0, self.config_data.get("detector_api_key", ""))
        self.cb_model_det.set(self.config_data.get("model_detector", "gemini-1.5-flash"))
        
        self.cb_prov_trans.set(self.config_data.get("provider_translator", "Google Gemini"))
        self.ent_trans_key.delete(0, "end")
        self.ent_trans_key.insert(0, self.config_data.get("translator_api_key", ""))
        self.cb_model_trans.set(self.config_data.get("model_translator", "gemini-1.5-flash"))
        
        self.cb_prov_rev.set(self.config_data.get("provider_reviewer", "Google Gemini"))
        self.ent_rev_key.delete(0, "end")
        self.ent_rev_key.insert(0, self.config_data.get("reviewer_api_key", ""))
        self.cb_model_rev.set(self.config_data.get("model_reviewer", "gemini-1.5-pro"))
        
        self.ent_batch.delete(0, "end")
        self.ent_batch.insert(0, str(self.config_data.get("batch_size", 5)))
