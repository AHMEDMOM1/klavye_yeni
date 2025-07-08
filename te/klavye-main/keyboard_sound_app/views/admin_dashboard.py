# views/admin_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
from keyboard_sound_app.utils.styles import Styles

class AdminDashboard:
    def __init__(self, admin_controller):
        self.controller = admin_controller
        self.styles = Styles()
        self.window = tk.Toplevel()
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        self.window.title("Yönetici Paneli - Kullanıcı Yönetimi")
        self.window.geometry("900x700")
        self.window.resizable(True, True)
        
        # Pencereyi ortala
        self.center_window()
        
        # Pencere kapatma olayını yakala
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Fontları ayarla
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.subtitle_font = font.Font(family="Arial", size=12, weight="bold")
        self.normal_font = font.Font(family="Arial", size=10)
        
        # Ana frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık ve istatistikler
        self.create_header(main_frame)
        
        # Arama ve filtreler
        self.create_search_section(main_frame)
        
        # Kullanıcı tablosu
        self.create_user_table(main_frame)
        
        # Butonlar
        self.create_button_section(main_frame)
        
        # Durum çubuğu
        self.create_status_bar(main_frame)

    def create_header(self, parent):
        """Başlık ve istatistik bölümü"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Ana başlık
        title_label = ttk.Label(header_frame, text="Kullanıcı Yönetim Paneli", 
                               font=self.title_font, foreground="blue")
        title_label.pack(side=tk.TOP, pady=(0, 10))
        
        # İstatistikler frame
        stats_frame = ttk.LabelFrame(header_frame, text="Sistem İstatistikleri", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # İstatistik labelları
        self.total_users_label = ttk.Label(stats_frame, text="Toplam Kullanıcı: 0", 
                                          font=self.normal_font)
        self.total_users_label.pack(side=tk.LEFT, padx=20)
        
        self.admin_users_label = ttk.Label(stats_frame, text="Admin: 0", 
                                          font=self.normal_font, foreground="red")
        self.admin_users_label.pack(side=tk.LEFT, padx=20)
        
        self.regular_users_label = ttk.Label(stats_frame, text="Normal: 0", 
                                           font=self.normal_font, foreground="green")
        self.regular_users_label.pack(side=tk.LEFT, padx=20)

    def create_search_section(self, parent):
        """Arama ve filtre bölümü"""
        search_frame = ttk.LabelFrame(parent, text="Arama ve Filtreler", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Arama satırı
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_row, text="Kullanıcı Ara:", font=self.normal_font).pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_row, font=self.normal_font, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Arama butonları
        search_btn = ttk.Button(search_row, text="Ara", command=self.search_users, width=8)
        search_btn.pack(side=tk.LEFT, padx=3)
        
        clear_btn = ttk.Button(search_row, text="Temizle", command=self.clear_search, width=8)
        clear_btn.pack(side=tk.LEFT, padx=3)
        
        refresh_btn = ttk.Button(search_row, text="Yenile", command=self.load_users, width=8)
        refresh_btn.pack(side=tk.LEFT, padx=3)
        
        # Filtre satırı
        filter_row = ttk.Frame(search_frame)
        filter_row.pack(fill=tk.X)
        
        ttk.Label(filter_row, text="Filtre:", font=self.normal_font).pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_row, text="Tümü", variable=self.filter_var, 
                       value="all", command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_row, text="Adminler", variable=self.filter_var, 
                       value="admin", command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_row, text="Normal Kullanıcılar", variable=self.filter_var, 
                       value="normal", command=self.apply_filter).pack(side=tk.LEFT, padx=5)

    def create_user_table(self, parent):
        """Kullanıcı tablosu"""
        table_frame = ttk.LabelFrame(parent, text="Kullanıcı Listesi", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Tablo container
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tablo sütunları
        columns = ("ID", "Kullanıcı Adı", "Son Giriş", "Giriş Sayısı", "Admin", "Oluşturulma Tarihi")
        self.users_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Sütun başlıkları ve genişlikleri
        self.users_tree.heading("ID", text="ID")
        self.users_tree.heading("Kullanıcı Adı", text="Kullanıcı Adı")
        self.users_tree.heading("Son Giriş", text="Son Giriş")
        self.users_tree.heading("Giriş Sayısı", text="Giriş Sayısı")
        self.users_tree.heading("Admin", text="Admin")
        self.users_tree.heading("Oluşturulma Tarihi", text="Oluşturulma Tarihi")
        
        self.users_tree.column("ID", width=50, anchor=tk.CENTER)
        self.users_tree.column("Kullanıcı Adı", width=150, anchor=tk.W)
        self.users_tree.column("Son Giriş", width=130, anchor=tk.CENTER)
        self.users_tree.column("Giriş Sayısı", width=80, anchor=tk.CENTER)
        self.users_tree.column("Admin", width=60, anchor=tk.CENTER)
        self.users_tree.column("Oluşturulma Tarihi", width=130, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.users_tree.xview)
        
        self.users_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack tablo ve scrollbar
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tablo olayları
        self.users_tree.bind('<Double-1>', self.on_user_double_click)
        self.users_tree.bind('<Button-3>', self.show_context_menu)  # Sağ tık menüsü

    def create_button_section(self, parent):
        """Buton bölümü"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sol taraf butonları
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        
        add_btn = ttk.Button(left_buttons, text="Kullanıcı Ekle", command=self.add_user_dialog, 
                            width=15, style='Accent.TButton')
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(left_buttons, text="Düzenle", command=self.edit_user_dialog, 
                             width=15)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(left_buttons, text="Kullanıcı Sil", command=self.delete_user, 
                               width=15)
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Orta butonları
        middle_buttons = ttk.Frame(button_frame)
        middle_buttons.pack(side=tk.LEFT, padx=50)
        
        admin_btn = ttk.Button(middle_buttons, text="Admin Yetkileri", command=self.toggle_admin_status, 
                              width=15)
        admin_btn.pack(side=tk.LEFT, padx=5)
        
        password_btn = ttk.Button(middle_buttons, text="Şifre Değiştir", command=self.change_password_dialog, 
                                 width=15)
        password_btn.pack(side=tk.LEFT, padx=5)
        
        # Sağ taraf butonları
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        export_btn = ttk.Button(right_buttons, text="Dışa Aktar", command=self.export_users, 
                               width=12)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        exit_btn = ttk.Button(right_buttons, text="Çıkış", command=self.on_closing, 
                             width=12)
        exit_btn.pack(side=tk.RIGHT, padx=5)

    def create_status_bar(self, parent):
        """Durum çubuğu"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        separator = ttk.Separator(status_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = ttk.Label(status_frame, text="Hazır", font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Sağ tarafta zaman
        self.time_label = ttk.Label(status_frame, text="", font=('Arial', 9))
        self.time_label.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Zamanı güncelle
        self.update_time()

    def center_window(self):
        """Pencereyi ortala"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def update_time(self):
        """Zaman güncelle"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.window.after(1000, self.update_time)

    def show(self):
        """Pencereyi göster"""
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    # admin_dashboard.py - load_users metodunu güncelle
def load_users(self):
    """Kullanıcıları yükle - created_at olmadan"""
    try:
        # Tabloyu temizle
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Kullanıcıları al
        users = self.controller.get_all_users()
        
        # Tabloyu doldur
        for user in users:
            admin_status = "Evet" if user[4] else "Hayır"
            last_login = user[2] if user[2] else "Hiç giriş yapılmadı"
            
            self.users_tree.insert("", "end", values=(
                user[0],  # ID
                user[1],  # Username
                last_login,  # Last login
                user[3],  # Login count
                admin_status,  # Is admin
                "Bilinmiyor"  # Created at yerine sabit değer
            ))
        
        # İstatistikleri güncelle
        self.update_statistics()
        self.set_status(f"{len(users)} kullanıcı yüklendi")
        
    except Exception as e:
        print(f"Kullanıcı yükleme hatası: {e}")
        self.set_status("Kullanıcılar yükleme hatası")

    def update_statistics(self):
        """İstatistikleri güncelle"""
        try:
            stats = self.controller.get_system_stats()
            self.total_users_label.config(text=f"Toplam Kullanıcı: {stats['total_users']}")
            self.admin_users_label.config(text=f"Admin: {stats['admin_users']}")
            self.regular_users_label.config(text=f"Normal: {stats['regular_users']}")
        except Exception as e:
            print(f"İstatistik güncelleme hatası: {e}")

    # search_users ve diğer metodları da benzer şekilde güncelle
def search_users(self):
    """Kullanıcılarda ara - created_at olmadan"""
    search_term = self.search_entry.get().strip()
    
    if not search_term:
        self.load_users()
        return
    
    try:
        # Tabloyu temizle
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Arama yap
        users = self.controller.search_users(search_term)
        
        # Sonuçları göster
        for user in users:
            admin_status = "Evet" if user[4] else "Hayır"
            last_login = user[2] if user[2] else "Hiç giriş yapılmadı"
            
            self.users_tree.insert("", "end", values=(
                user[0], user[1], last_login, user[3], admin_status, "Bilinmiyor"
            ))
        
        self.set_status(f"'{search_term}' için {len(users)} sonuç bulundu")
        
    except Exception as e:
        print(f"Arama hatası: {e}")

    def clear_search(self):
        """Aramayı temizle"""
        self.search_entry.delete(0, tk.END)
        self.load_users()

    def apply_filter(self):
        """Filtre uygula"""
        filter_type = self.filter_var.get()
        
        try:
            # Tabloyu temizle
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Filtreye göre kullanıcıları al
            if filter_type == "admin":
                users = self.controller.get_admin_users()
            elif filter_type == "normal":
                users = self.controller.get_regular_users()
            else:
                users = self.controller.get_all_users()
            
            # Tabloyu doldur
            for user in users:
                admin_status = "Evet" if user[4] else "Hayır"
                last_login = user[2] if user[2] else "Hiç giriş yapılmadı"
                created_at = user[5] if len(user) > 5 and user[5] else "Bilinmiyor"
                
                self.users_tree.insert("", "end", values=(
                    user[0], user[1], last_login, user[3], admin_status, created_at
                ))
            
            self.set_status(f"{filter_type.title()} filtresi uygulandı - {len(users)} kullanıcı")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Filtre uygulanırken hata: {str(e)}")

    def get_selected_user(self):
        """Seçili kullanıcıyı al"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            return None
        
        user_data = self.users_tree.item(selected_item[0])["values"]
        return user_data

    def add_user_dialog(self):
        """Kullanıcı ekleme dialog'u"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Yeni Kullanıcı Ekle")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Dialogu ortala
        dialog.transient(self.window)
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        ttk.Label(main_frame, text="Yeni Kullanıcı Bilgileri", font=self.subtitle_font).pack(pady=(0, 20))
        
        # Form alanları
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(form_frame, text="Kullanıcı Adı:", font=self.normal_font).grid(row=0, column=0, padx=5, pady=10, sticky=tk.E)
        username_entry = ttk.Entry(form_frame, font=self.normal_font, width=25)
        username_entry.grid(row=0, column=1, padx=5, pady=10)
        
        ttk.Label(form_frame, text="Şifre:", font=self.normal_font).grid(row=1, column=0, padx=5, pady=10, sticky=tk.E)
        password_entry = ttk.Entry(form_frame, show="*", font=self.normal_font, width=25)
        password_entry.grid(row=1, column=1, padx=5, pady=10)
        
        ttk.Label(form_frame, text="Şifre Tekrar:", font=self.normal_font).grid(row=2, column=0, padx=5, pady=10, sticky=tk.E)
        password_confirm_entry = ttk.Entry(form_frame, show="*", font=self.normal_font, width=25)
        password_confirm_entry.grid(row=2, column=1, padx=5, pady=10)
        
        # Admin checkbox
        admin_var = tk.BooleanVar()
        admin_check = ttk.Checkbutton(form_frame, text="Admin Yetkisi Ver", variable=admin_var, 
                                     font=self.normal_font)
        admin_check.grid(row=3, column=1, padx=5, pady=10, sticky=tk.W)
        
        # Butonlar
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get()
            password_confirm = password_confirm_entry.get()
            
            if not username or not password:
                messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz")
                return
            
            if password != password_confirm:
                messagebox.showerror("Hata", "Şifreler eşleşmiyor")
                return
            
            success, message = self.controller.add_user(username, password, admin_var.get())
            if success:
                messagebox.showinfo("Başarılı", message)
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Hata", message)
        
        ttk.Button(button_frame, text="Kaydet", command=save_user, 
                  style='Accent.TButton', width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy, 
                  width=12).pack(side=tk.LEFT, padx=5)
        
        # Focus
        username_entry.focus()

    def edit_user_dialog(self):
        """Kullanıcı düzenleme dialog'u"""
        selected_user = self.get_selected_user()
        if not selected_user:
            messagebox.showwarning("Uyarı", "Lütfen düzenlemek için bir kullanıcı seçin")
            return
        
        user_id = selected_user[0]
        current_username = selected_user[1]
        
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Kullanıcı Düzenle: {current_username}")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Kullanıcı: {current_username}", font=self.subtitle_font).pack(pady=(0, 20))
        
        # Sadece admin durumunu düzenle
        current_admin = selected_user[4] == "Evet"
        admin_var = tk.BooleanVar(value=current_admin)
        admin_check = ttk.Checkbutton(main_frame, text="Admin Yetkisi", variable=admin_var, 
                                     font=self.normal_font)
        admin_check.pack(pady=10)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        def save_changes():
            success, message = self.controller.update_user_admin_status(user_id, admin_var.get())
            if success:
                messagebox.showinfo("Başarılı", message)
                dialog.destroy()
                self.load_users()
            else:
                messagebox.showerror("Hata", message)
        
        ttk.Button(button_frame, text="Kaydet", command=save_changes, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def delete_user(self):
        """Kullanıcı sil"""
        selected_user = self.get_selected_user()
        if not selected_user:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir kullanıcı seçin")
            return
        
        user_id = selected_user[0]
        username = selected_user[1]
        
        if messagebox.askyesno("Silme Onayı", 
                              f"'{username}' kullanıcısını silmek istediğinizden emin misiniz?\n\nBu işlem geri alınamaz."):
            success, message = self.controller.delete_user(user_id)
            if success:
                messagebox.showinfo("Başarılı", message)
                self.load_users()
            else:
                messagebox.showerror("Hata", message)

    def toggle_admin_status(self):
        """Admin durumunu değiştir"""
        selected_user = self.get_selected_user()
        if not selected_user:
            messagebox.showwarning("Uyarı", "Lütfen bir kullanıcı seçin")
            return
        
        user_id = selected_user[0]
        username = selected_user[1]
        current_admin = selected_user[4] == "Evet"
        
        new_admin_status = not current_admin
        action = "kaldır" if current_admin else "ver"
        
        if messagebox.askyesno("Admin Yetkisi", 
                              f"'{username}' kullanıcısına admin yetkisi {action}mak istediğinizden emin misiniz?"):
            success, message = self.controller.update_user_admin_status(user_id, new_admin_status)
            if success:
                messagebox.showinfo("Başarılı", message)
                self.load_users()
            else:
                messagebox.showerror("Hata", message)

    def change_password_dialog(self):
        """Şifre değiştirme dialog'u"""
        selected_user = self.get_selected_user()
        if not selected_user:
            messagebox.showwarning("Uyarı", "Lütfen kullanıcı seçin")
            return
        
        user_id = selected_user[0]
        username = selected_user[1]
        
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Şifre Değiştir: {username}")
        dialog.geometry("350x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text=f"Kullanıcı: {username}", font=self.subtitle_font).pack(pady=(0, 15))
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(form_frame, text="Yeni Şifre:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        new_password_entry = ttk.Entry(form_frame, show="*", width=20)
        new_password_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Şifre Tekrar:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        confirm_password_entry = ttk.Entry(form_frame, show="*", width=20)
        confirm_password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        def change_password():
            new_password = new_password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if not new_password:
                messagebox.showerror("Hata", "Yeni şifre boş olamaz")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Hata", "Şifreler eşleşmiyor")
                return
            
            success, message = self.controller.update_user_password(user_id, new_password)
            if success:
                messagebox.showinfo("Başarılı", message)
                dialog.destroy()
            else:
                messagebox.showerror("Hata", message)
        
        ttk.Button(button_frame, text="Değiştir", command=change_password, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="İptal", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        new_password_entry.focus()

    def on_user_double_click(self, event):
        """Kullanıcıya çift tıklandığında"""
        self.edit_user_dialog()

    def show_context_menu(self, event):
        """Sağ tık menüsü"""
        # Gelecekte implement edilebilir
        pass

    def export_users(self):
        """Kullanıcıları dışa aktar"""
        # Gelecekte implement edilebilir
        messagebox.showinfo("Bilgi", "Dışa aktarma özelliği yakında eklenecek")

    def refresh_data(self):
        """Verileri yenile"""
        self.load_users()
        self.update_statistics()
        self.set_status("Veriler yenilendi")

    def set_status(self, message):
        """Durum mesajını ayarla"""
        self.status_label.config(text=message)
        # 5 saniye sonra "Hazır" durumuna dön
        self.window.after(5000, lambda: self.status_label.config(text="Hazır"))

    def on_closing(self):
        """Pencere kapatılırken"""
        if messagebox.askyesno("Çıkış", "Admin panelini kapatmak istediğinizden emin misiniz?"):
            self.window.destroy()
            
            # Ana uygulamayı tekrar göster (opsiyonel)
            try:
                if hasattr(self.controller, 'app_controller'):
                    self.controller.app_controller.show_login_window()
            except:
                pass

    def minimize_window(self):
        """Pencereyi küçült"""
        self.window.iconify()

    def maximize_window(self):
        """Pencereyi büyüt"""
        self.window.state('zoomed')

    def restore_window(self):
        """Pencereyi geri yükle"""
        self.window.state('normal')

    def get_window_state(self):
        """Pencere durumunu al"""
        return self.window.state()

    def set_window_state(self, state):
        """Pencere durumunu ayarla"""
        self.window.state(state)

    def focus_search(self):
        """Arama alanına focus ver"""
        self.search_entry.focus()

    def clear_selection(self):
        """Seçimi temizle"""
        self.users_tree.selection_remove(self.users_tree.selection())

    def select_first_user(self):
        """İlk kullanıcıyı seç"""
        children = self.users_tree.get_children()
        if children:
            self.users_tree.selection_set(children[0])
            self.users_tree.focus(children[0])

    def select_last_user(self):
        """Son kullanıcıyı seç"""
        children = self.users_tree.get_children()
        if children:
            self.users_tree.selection_set(children[-1])
            self.users_tree.focus(children[-1])

    def get_selected_user_count(self):
        """Seçili kullanıcı sayısını al"""
        return len(self.users_tree.selection())

    def get_all_users_data(self):
        """Tüm kullanıcı verilerini al"""
        users_data = []
        for child in self.users_tree.get_children():
            user_data = self.users_tree.item(child)["values"]
            users_data.append(user_data)
        return users_data

    def sort_users_by_column(self, column):
        """Kullanıcıları sütuna göre sırala"""
        # Gelecekte implement edilebilir
        pass

    def show_user_details(self, user_id):
        """Kullanıcı detaylarını göster"""
        try:
            user_details = self.controller.get_user_details(user_id)
            if user_details:
                detail_window = tk.Toplevel(self.window)
                detail_window.title(f"Kullanıcı Detayları: {user_details['username']}")
                detail_window.geometry("400x300")
                detail_window.resizable(False, False)
                detail_window.grab_set()
                
                main_frame = ttk.Frame(detail_window, padding="20")
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # Kullanıcı bilgileri
                info_frame = ttk.LabelFrame(main_frame, text="Kullanıcı Bilgileri", padding="10")
                info_frame.pack(fill=tk.X, pady=(0, 10))
                
                ttk.Label(info_frame, text=f"ID: {user_details['id']}").pack(anchor=tk.W, pady=2)
                ttk.Label(info_frame, text=f"Kullanıcı Adı: {user_details['username']}").pack(anchor=tk.W, pady=2)
                ttk.Label(info_frame, text=f"Admin: {'Evet' if user_details['is_admin'] else 'Hayır'}").pack(anchor=tk.W, pady=2)
                ttk.Label(info_frame, text=f"Giriş Sayısı: {user_details['login_count']}").pack(anchor=tk.W, pady=2)
                ttk.Label(info_frame, text=f"Son Giriş: {user_details['last_login'] or 'Hiç giriş yapılmadı'}").pack(anchor=tk.W, pady=2)
                ttk.Label(info_frame, text=f"Oluşturulma: {user_details['created_at'] or 'Bilinmiyor'}").pack(anchor=tk.W, pady=2)
                
                # Kapat butonu
                ttk.Button(main_frame, text="Kapat", command=detail_window.destroy).pack(pady=10)
                
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcı detayları alınırken hata: {str(e)}")

    def backup_users(self):
        """Kullanıcıları yedekle"""
        # Gelecekte implement edilebilir
        messagebox.showinfo("Bilgi", "Yedekleme özelliği yakında eklenecek")

    def restore_users(self):
        """Kullanıcıları geri yükle"""
        # Gelecekte implement edilebilir
        messagebox.showinfo("Bilgi", "Geri yükleme özelliği yakında eklenecek")

    def validate_user_data(self, username, password):
        """Kullanıcı verilerini doğrula"""
        if not username or len(username) < 3:
            return False, "Kullanıcı adı en az 3 karakter olmalıdır"
        
        if not password or len(password) < 3:
            return False, "Şifre en az 3 karakter olmalıdır"
        
        # Özel karakterler kontrolü
        import re
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "Kullanıcı adı sadece harf, rakam ve alt çizgi içerebilir"
        
        return True, "Geçerli"

    def reset_filters(self):
        """Filtreleri sıfırla"""
        self.filter_var.set("all")
        self.search_entry.delete(0, tk.END)
        self.load_users()

    def get_user_statistics(self):
        """Kullanıcı istatistiklerini al"""
        try:
            return self.controller.get_system_stats()
        except Exception as e:
            print(f"İstatistik alma hatası: {e}")
            return {"total_users": 0, "admin_users": 0, "regular_users": 0}

    def refresh_statistics(self):
        """İstatistikleri yenile"""
        self.update_statistics()

    def set_theme(self, theme):
        """Tema ayarla"""
        # Gelecekte implement edilebilir
        pass

    def get_theme(self):
        """Mevcut temayı al"""
        # Gelecekte implement edilebilir
        return "default"

    def show_help(self):
        """Yardım penceresi göster"""
        help_window = tk.Toplevel(self.window)
        help_window.title("Yardım")
        help_window.geometry("500x400")
        help_window.resizable(False, False)
        help_window.grab_set()
        
        main_frame = ttk.Frame(help_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = """
        KULLANICI YÖNETİM PANELİ YARDIM
        
        Temel İşlemler:
        • Kullanıcı Ekle: Yeni kullanıcı oluşturmak için
        • Kullanıcı Sil: Seçili kullanıcıyı silmek için
        • Düzenle: Kullanıcı bilgilerini düzenlemek için
        • Admin Yetkileri: Admin yetkilerini değiştirmek için
        
        Arama ve Filtreleme:
        • Arama kutusu ile kullanıcı adına göre arama yapabilirsiniz
        • Filtre seçenekleri ile kullanıcı tipine göre filtreleme yapabilirsiniz
        
        Klavye Kısayolları:
        • Enter: Arama yap
        • Escape: Aramayı temizle
        • F5: Listeyi yenile
        
        Güvenlik:
        • Ana admin kullanıcısı (Admin123) silinemez
        • Şifre değişiklikleri hemen etkili olur
        • Tüm işlemler loglanır
        """
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, font=self.normal_font)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Kapat", command=help_window.destroy).pack(pady=10)

    def show_about(self):
        """Hakkında penceresi göster"""
        about_window = tk.Toplevel(self.window)
        about_window.title("Hakkında")
        about_window.geometry("350x250")
        about_window.resizable(False, False)
        about_window.grab_set()
        
        main_frame = ttk.Frame(about_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Klavye Ses Uygulaması", font=self.title_font).pack(pady=10)
        ttk.Label(main_frame, text="Admin Paneli", font=self.subtitle_font).pack(pady=5)
        ttk.Label(main_frame, text="Versiyon 1.0", font=self.normal_font).pack(pady=5)
        ttk.Label(main_frame, text="Kullanıcı yönetimi için geliştirilmiştir", font=self.normal_font).pack(pady=10)
        
        ttk.Button(main_frame, text="Kapat", command=about_window.destroy).pack(pady=20)

    def __del__(self):
        """Destructor"""
        try:
            if hasattr(self, 'window') and self.window:
                self.window.destroy()
        except:
            pass