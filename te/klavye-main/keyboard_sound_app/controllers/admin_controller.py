# admin_controller.py
import tkinter as tk
from tkinter import messagebox
from keyboard_sound_app.views.admin_dashboard import AdminDashboard
from keyboard_sound_app.models.user_model import UserModel

class AdminController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.user_model = UserModel()
        self.admin_dashboard = None
        self.current_admin_user = None
        
    def set_current_admin(self, admin_user):
        """Mevcut admin kullanıcısını ayarla"""
        self.current_admin_user = admin_user
        
    def show_admin_dashboard(self):
        """Admin panelini göster"""
        if self.admin_dashboard is None or not self.admin_dashboard.window.winfo_exists():
            self.admin_dashboard = AdminDashboard(self)
            self.admin_dashboard.show()
        else:
            self.admin_dashboard.window.lift()
            self.admin_dashboard.window.focus_force()
    
    def get_all_users(self):
        """Tüm kullanıcıları getir"""
        try:
            users = self.user_model.get_all_users()
            return users if users else []
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcılar alınırken hata oluştu: {str(e)}")
            return []
    
    def get_users_count(self):
        """Toplam kullanıcı sayısını getir"""
        try:
            return self.user_model.get_users_count()
        except Exception as e:
            print(f"Kullanıcı sayısı alınırken hata: {e}")
            return 0
    
    def get_admin_users(self):
        """Sadece admin kullanıcıları getir"""
        try:
            return self.user_model.get_admin_users()
        except Exception as e:
            messagebox.showerror("Hata", f"Admin kullanıcıları alınırken hata: {str(e)}")
            return []
    
    def get_regular_users(self):
        """Sadece normal kullanıcıları getir"""
        try:
            return self.user_model.get_regular_users()
        except Exception as e:
            messagebox.showerror("Hata", f"Normal kullanıcılar alınırken hata: {str(e)}")
            return []
    
    def add_user(self, username, password, is_admin=False):
        """Yeni kullanıcı ekle"""
        if not username or not password:
            return False, "Kullanıcı adı ve şifre boş olamaz"
        
        if len(username) < 3:
            return False, "Kullanıcı adı en az 3 karakter olmalıdır"
        
        if len(password) < 3:
            return False, "Şifre en az 3 karakter olmalıdır"
        
        if self.user_model.user_exists(username):
            return False, "Bu kullanıcı adı zaten mevcut"
        
        try:
            success = self.user_model.create_user(username, password, is_admin)
            if success:
                return True, "Kullanıcı başarıyla eklendi"
            else:
                return False, "Kullanıcı eklenirken hata oluştu"
        except Exception as e:
            return False, f"Veritabanı hatası: {str(e)}"
    
    def delete_user(self, user_id):
        """Kullanıcı sil"""
        if not user_id:
            return False, "Geçersiz kullanıcı ID"
        
        try:
            # Kullanıcı bilgilerini al
            user = self.user_model.get_user_by_id(user_id)
            if not user:
                return False, "Kullanıcı bulunamadı"
            
            # Admin123 kullanıcısını silmeye izin verme
            if user[1] == "Admin123":  # username sütunu
                return False, "Ana admin kullanıcısı silinemez"
            
            success, message = self.user_model.delete_user(user_id)
            return success, message
        except Exception as e:
            return False, f"Silme işlemi sırasında hata: {str(e)}"
    
    def search_users(self, search_term):
        """Kullanıcılarda ara"""
        if not search_term:
            return self.get_all_users()
        
        try:
            return self.user_model.search_users(search_term)
        except Exception as e:
            messagebox.showerror("Hata", f"Arama sırasında hata: {str(e)}")
            return []
    
    def update_user_admin_status(self, user_id, is_admin):
        """Kullanıcının admin durumunu güncelle"""
        if not user_id:
            return False, "Geçersiz kullanıcı ID"
        
        try:
            success, message = self.user_model.update_user_role(user_id, is_admin)
            return success, message
        except Exception as e:
            return False, f"Güncelleme sırasında hata: {str(e)}"
    
    def update_user_password(self, user_id, new_password):
        """Kullanıcı şifresini güncelle"""
        if not user_id:
            return False, "Geçersiz kullanıcı ID"
        
        if not new_password or len(new_password) < 3:
            return False, "Şifre en az 3 karakter olmalıdır"
        
        try:
            success, message = self.user_model.update_user_password(user_id, new_password)
            return success, message
        except Exception as e:
            return False, f"Şifre güncelleme sırasında hata: {str(e)}"
    
    def get_user_details(self, user_id):
        """Kullanıcı detaylarını getir"""
        try:
            user = self.user_model.get_user_by_id(user_id)
            if user:
                return {
                    "id": user[0],
                    "username": user[1],
                    "password": user[2],
                    "last_login": user[3],
                    "login_count": user[4],
                    "is_admin": bool(user[5]),
                    "created_at": user[6] if len(user) > 6 else None
                }
            return None
        except Exception as e:
            print(f"Kullanıcı detayları alınırken hata: {e}")
            return None
    
    def get_user_login_history(self, user_id):
        """Kullanıcının giriş geçmişini getir"""
        try:
            return self.user_model.get_user_login_history(user_id)
        except Exception as e:
            print(f"Giriş geçmişi alınırken hata: {e}")
            return None
    
    def validate_admin_credentials(self, username, password):
        """Admin kimlik bilgilerini doğrula"""
        # Özel admin123 kontrolü
        if username == "admin123" and password == "admin123":
            return True, {"username": "admin123", "is_admin": True}
        
        # Veritabanından admin kullanıcılarını kontrol et
        try:
            auth_result = self.user_model.authenticate(username, password)
            if auth_result and auth_result.get("is_admin"):
                return True, auth_result
            return False, None
        except Exception as e:
            print(f"Admin doğrulama hatası: {e}")
            return False, None
    
    def get_system_stats(self):
        """Sistem istatistiklerini getir"""
        try:
            total_users = self.user_model.get_users_count()
            admin_users = len(self.user_model.get_admin_users())
            regular_users = len(self.user_model.get_regular_users())
            
            return {
                "total_users": total_users,
                "admin_users": admin_users,
                "regular_users": regular_users
            }
        except Exception as e:
            print(f"Sistem istatistikleri alınırken hata: {e}")
            return {
                "total_users": 0,
                "admin_users": 0,
                "regular_users": 0
            }
    
    def close_admin_dashboard(self):
        """Admin panelini kapat"""
        if self.admin_dashboard:
            self.admin_dashboard.window.destroy()
            self.admin_dashboard = None
    
    def refresh_dashboard(self):
        """Dashboard'u yenile"""
        if self.admin_dashboard:
            self.admin_dashboard.refresh_data()
    
    def export_users_data(self):
        """Kullanıcı verilerini dışa aktar (gelecekteki özellik)"""
        # Bu özellik gelecekte implement edilebilir
        pass
    
    def import_users_data(self):
        """Kullanıcı verilerini içe aktar (gelecekteki özellik)"""
        # Bu özellik gelecekte implement edilebilir
        pass
