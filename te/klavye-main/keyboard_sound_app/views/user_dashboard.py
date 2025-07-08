# views/user_dashboard.py
import tkinter as tk
from tkinter import ttk
from keyboard_sound_app.utils.styles import Styles

class UserDashboard:
    def __init__(self, root):
        self.root = root
        self.styles = Styles()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Kullanıcı Paneli")
        self.root.geometry("600x400")
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Kullanıcı Paneline Hoş Geldiniz", style='Title.TLabel').pack(pady=20)
        
        # Kullanıcı bilgileri
        info_frame = ttk.LabelFrame(main_frame, text="Hesap Bilgileriniz")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text="Kullanıcı Adı: user123").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text="Son Giriş: 2023-10-15 14:30").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(info_frame, text="Giriş Sayısı: 12").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Uygulama ayarları
        settings_frame = ttk.LabelFrame(main_frame, text="Uygulama Ayarları")
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        volume_label = ttk.Label(settings_frame, text="Ses Seviyesi:")
        volume_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        volume_scale = ttk.Scale(settings_frame, from_=0, to=100)
        volume_scale.set(80)  # Varsayılan değer
        volume_scale.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # İşlem butonları
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        logout_button = ttk.Button(button_frame, text="Çıkış Yap", command=self.logout)
        logout_button.pack(side=tk.RIGHT, padx=5)

    def logout(self):
        # Giriş ekranını tekrar göster
        for widget in self.root.winfo_children():
            widget.destroy()
        
        from keyboard_sound_app.views.login_view import LoginView
        from keyboard_sound_app.controllers.login_controller import LoginController
        login_controller = LoginController(self.root)
        LoginView(self.root, login_controller)