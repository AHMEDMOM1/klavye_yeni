import tkinter as tk
from tkinter import ttk, filedialog
from keyboard_sound_app.utils.styles import Styles

class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.styles = Styles()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Klavye Ses Uygulaması")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Klavye Ses Uygulaması", style='Title.TLabel').pack(side=tk.LEFT)
        
        self.user_label = ttk.Label(header_frame, text="", style='TLabel')
        self.user_label.pack(side=tk.RIGHT)
        
        settings_frame = ttk.LabelFrame(main_frame, text="Ses Ayarları", padding="15")
        settings_frame.pack(fill=tk.X, pady=10)
        
        file_frame = ttk.Frame(settings_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(file_frame, text="Ses Dosyası:").pack(side=tk.LEFT)
        self.file_path_entry = ttk.Entry(file_frame, state='readonly')
        self.file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_button = ttk.Button(file_frame, text="Gözat", command=self.on_browse)
        browse_button.pack(side=tk.LEFT)
        
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        preview_button = ttk.Button(button_frame, text="Önizleme", command=self.on_preview, style='Accent.TButton')
        preview_button.pack(side=tk.LEFT, padx=5)
        
        stop_button = ttk.Button(button_frame, text="Durdur", command=self.on_stop, style='Danger.TButton')
        stop_button.pack(side=tk.LEFT, padx=5)
        
        save_button = ttk.Button(button_frame, text="Kaydet", command=self.on_save)
        save_button.pack(side=tk.LEFT, padx=5)
        
        exit_button = ttk.Button(main_frame, text="Çıkış", command=self.on_exit, style='Danger.TButton')
        exit_button.pack(side=tk.BOTTOM, pady=20)

    def on_browse(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav"), ("All Files", "*.*")])
        if file_path:
            self.file_path_entry.config(state='normal')
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            self.file_path_entry.config(state='readonly')
            self.controller.preview_sound(file_path)

    def on_preview(self):
        self.controller.preview_sound(self.file_path_entry.get())

    def on_stop(self):
        self.controller.stop_sound()

    def on_save(self):
        file_path = self.file_path_entry.get()
        if file_path:
            self.controller.save_settings(file_path)

    def on_exit(self):
        self.controller.exit_app()

    def set_user_info(self, username, login_count, last_login):
        info_text = f"{username} | Giriş: {login_count} | Son: {last_login}"
        self.user_label.config(text=info_text)

    def set_file_path(self, file_path):
        self.file_path_entry.config(state='normal')
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)
        self.file_path_entry.config(state='readonly')