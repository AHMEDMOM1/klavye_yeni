# login_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from keyboard_sound_app.utils.styles import Styles

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.styles = Styles()
        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        self.root.title("Klavye Ses Uygulaması - Giriş")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        # Pencereyi ortala
        self.center_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="Klavye Ses Uygulaması", style='Title.TLabel')
        title_label.pack(pady=15)
        
        # Alt başlık
        subtitle_label = ttk.Label(main_frame, text="Giriş Yapın", style='Subtitle.TLabel')
        subtitle_label.pack(pady=5)
        
        # Form alanı
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(pady=30)
        
        # Kullanıcı adı
        ttk.Label(form_frame, text="Kullanıcı Adı:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.E)
        self.username_entry = ttk.Entry(form_frame, width=20, font=('Arial', 10))
        self.username_entry.grid(row=0, column=1, padx=5, pady=10)
        
        # Şifre
        ttk.Label(form_frame, text="Şifre:").grid(row=1, column=0, padx=5, pady=10, sticky=tk.E)
        self.password_entry = ttk.Entry(form_frame, show="*", width=20, font=('Arial', 10))
        self.password_entry.grid(row=1, column=1, padx=5, pady=10)
        
        # Giriş türü seçimi (opsiyonel)
        ttk.Label(form_frame, text="Giriş Türü:").grid(row=2, column=0, padx=5, pady=10, sticky=tk.E)
        self.login_type_var = tk.StringVar(value="normal")
        login_type_frame = ttk.Frame(form_frame)
        login_type_frame.grid(row=2, column=1, padx=5, pady=10)
        
        ttk.Radiobutton(login_type_frame, text="Normal", variable=self.login_type_var, 
                       value="normal").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(login_type_frame, text="Admin", variable=self.login_type_var, 
                       value="admin").pack(side=tk.LEFT, padx=5)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=25)
        
        # Giriş butonu
        login_button = ttk.Button(button_frame, text="Giriş Yap", command=self.on_login, 
                                 style='Accent.TButton', width=12)
        login_button.pack(side=tk.LEFT, padx=8)
        
        # Kayıt ol butonu
        register_button = ttk.Button(button_frame, text="Kayıt Ol", command=self.on_register, 
                                   width=12)
        register_button.pack(side=tk.LEFT, padx=8)
        
        # Temizle butonu
        clear_button = ttk.Button(button_frame, text="Temizle", command=self.clear_entries, 
                                width=12)
        clear_button.pack(side=tk.LEFT, padx=8)
        
        # Hata mesajı alanı
        self.error_label = ttk.Label(main_frame, text="", foreground="red", font=('Arial', 9))
        self.error_label.pack(pady=10)
        
        # Başarı mesajı alanı
        self.success_label = ttk.Label(main_frame, text="", foreground="green", font=('Arial', 9))
        self.success_label.pack()
        
        # Durum çubuğu
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Giriş yapmak için bilgilerinizi girin", 
                                     font=('Arial', 8))
        self.status_label.pack(side=tk.LEFT)

    def bind_events(self):
        """Klavye olaylarını bağla"""
        self.root.bind('<Return>', lambda event: self.on_login())
        self.root.bind('<Escape>', lambda event: self.clear_entries())
        
        # Entry alanlarına focus olayları
        self.username_entry.bind('<FocusIn>', lambda event: self.clear_messages())
        self.password_entry.bind('<FocusIn>', lambda event: self.clear_messages())

    def center_window(self):
        """Pencereyi ekranın ortasına konumlandır"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def on_login(self):
        """Giriş yapma işlemi"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Boş alan kontrolü
        if not username or not password:
            self.show_error("Kullanıcı adı ve şifre boş olamaz")
            return
        
        # Mesajları temizle
        self.clear_messages()
        self.set_status("Giriş yapılıyor...")
        
        # Özel admin girişi kontrolü
        if username == "admin123" and password == "admin123":
            self.show_success("Admin girişi başarılı!")
            self.set_status("Admin paneline yönlendiriliyor...")
            self.root.after(1000, lambda: self.handle_admin_login("admin123"))
            return
        
        # Veritabanından kullanıcı kontrolü
        try:
            success, user_data = self.controller.login(username, password)
            
            if success:
                if user_data.get('is_admin'):
                    self.show_success("Admin girişi başarılı!")
                    self.set_status("Admin paneline yönlendiriliyor...")
                    self.root.after(1000, lambda: self.handle_admin_login(user_data['username']))
                else:
                    self.show_success("Giriş başarılı!")
                    self.set_status("Ana uygulamaya yönlendiriliyor...")
                    self.root.after(1000, lambda: self.handle_user_login(user_data))
            else:
                self.show_error("Kullanıcı adı veya şifre yanlış")
                self.set_status("Giriş başarısız")
        except Exception as e:
            self.show_error(f"Giriş sırasında hata oluştu: {str(e)}")
            self.set_status("Hata oluştu")

    def handle_admin_login(self, username):
        """Admin girişini işle"""
        try:
            # Admin controller'a mevcut admin kullanıcısını set et
            if hasattr(self.controller, 'admin_controller'):
                self.controller.admin_controller.set_current_admin({"username": username, "is_admin": True})
            
            # Ana pencereyi gizle
            self.root.withdraw()
            
            # Admin dashboard'ı göster
            self.controller.show_admin_dashboard()
            
        except Exception as e:
            self.show_error(f"Admin paneli açılırken hata: {str(e)}")
            self.root.deiconify()

    def handle_user_login(self, user_data):
        """Normal kullanıcı girişini işle"""
        try:
            # Ana pencereyi gizle
            self.root.withdraw()
            
            # Ana uygulamayı göster
            self.controller.show_main_application(user_data)
            
        except Exception as e:
            self.show_error(f"Ana uygulama açılırken hata: {str(e)}")
            self.root.deiconify()

    def on_register(self):
        """Kayıt olma işlemi"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Boş alan kontrolü
        if not username or not password:
            self.show_error("Kullanıcı adı ve şifre boş olamaz")
            return
        
        # Minimum uzunluk kontrolü
        if len(username) < 3:
            self.show_error("Kullanıcı adı en az 3 karakter olmalıdır")
            return
        
        if len(password) < 3:
            self.show_error("Şifre en az 3 karakter olmalıdır")
            return
        
        # Mesajları temizle
        self.clear_messages()
        self.set_status("Kayıt yapılıyor...")
        
        try:
            # Admin kaydı mı?
            is_admin = self.login_type_var.get() == "admin"
            
            success, message = self.controller.register(username, password, is_admin)
            
            if success:
                self.show_success(message)
                self.set_status("Kayıt başarılı")
                # Formu temizle
                self.root.after(2000, self.clear_entries)
            else:
                self.show_error(message)
                self.set_status("Kayıt başarısız")
        except Exception as e:
            self.show_error(f"Kayıt sırasında hata oluştu: {str(e)}")
            self.set_status("Hata oluştu")

    def show_error(self, message):
        """Hata mesajı göster"""
        self.success_label.config(text="")
        self.error_label.config(text=message)
        # 5 saniye sonra mesajı temizle
        self.root.after(5000, lambda: self.error_label.config(text=""))

    def show_success(self, message):
        """Başarı mesajı göster"""
        self.error_label.config(text="")
        self.success_label.config(text=message)
        # 3 saniye sonra mesajı temizle
        self.root.after(3000, lambda: self.success_label.config(text=""))

    def clear_messages(self):
        """Tüm mesajları temizle"""
        self.error_label.config(text="")
        self.success_label.config(text="")

    def set_status(self, message):
        """Durum mesajını güncelle"""
        self.status_label.config(text=message)

    def clear_entries(self):
        """Giriş alanlarını temizle"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.login_type_var.set("normal")
        self.clear_messages()
        self.set_status("Giriş yapmak için bilgilerinizi girin")
        self.username_entry.focus()

    def focus_username(self):
        """Kullanıcı adı alanına focus ver"""
        self.username_entry.focus()

    def focus_password(self):
        """Şifre alanına focus ver"""
        self.password_entry.focus()

    def get_credentials(self):
        """Mevcut giriş bilgilerini al"""
        return {
            "username": self.username_entry.get().strip(),
            "password": self.password_entry.get().strip(),
            "login_type": self.login_type_var.get()
        }

    def set_credentials(self, username="", password=""):
        """Giriş bilgilerini ayarla"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.password_entry.insert(0, password)

    def disable_form(self):
        """Formu devre dışı bırak"""
        self.username_entry.config(state='disabled')
        self.password_entry.config(state='disabled')

    def enable_form(self):
        """Formu etkinleştir"""
        self.username_entry.config(state='normal')
        self.password_entry.config(state='normal')