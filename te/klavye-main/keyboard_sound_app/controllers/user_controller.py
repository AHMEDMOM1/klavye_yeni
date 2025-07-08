# user_controller.py
from keyboard_sound_app.models.user_model import UserModel

class UserController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.model = UserModel()

    def login(self, username, password):
        """تسجيل الدخول - يرجع user data أو None"""
        try:
            # استخدام authenticate من UserModel
            auth_result = self.model.authenticate(username, password)
            
            if auth_result:
                # auth_result يحتوي على {"id": user_id, "username": username, "is_admin": bool}
                return auth_result
            else:
                return None
                
        except Exception as e:
            print(f"Login controller hatası: {e}")
            return None

    def register(self, username, password, is_admin=False):
        """التسجيل - مع دعم admin parameter"""
        try:
            # التحقق من صحة البيانات
            if not username or not password:
                return False, "Kullanıcı adı ve şifre boş olamaz"
            
            if len(username) < 3:
                return False, "Kullanıcı adı en az 3 karakter olmalıdır"
            
            if len(password) < 4:
                return False, "Şifre en az 4 karakter olmalı"
            
            # التحقق من وجود المستخدم
            if self.model.user_exists(username):
                return False, "Bu kullanıcı adı zaten alınmış"
            
            # إنشاء المستخدم
            success = self.model.create_user(username, password, is_admin)
            
            if success:
                return True, "Kayıt başarılı. Giriş yapabilirsiniz."
            else:
                return False, "Kayıt sırasında hata oluştu"
                
        except Exception as e:
            print(f"Register controller hatası: {e}")
            return False, f"Kayıt hatası: {str(e)}"

    def get_user_data(self, username):
        """Kullanıcı verilerini al"""
        try:
            return self.model.get_user_by_username(username)
        except Exception as e:
            print(f"Kullanıcı verisi alma hatası: {e}")
            return None

    def get_user_stats(self, username):
        """Kullanıcı istatistiklerini al"""
        try:
            return self.model.get_user_stats(username)
        except Exception as e:
            print(f"Kullanıcı istatistikleri alma hatası: {e}")
            return None

    def authenticate_user(self, username, password):
        """Kullanıcı kimlik doğrulaması"""
        try:
            return self.model.authenticate(username, password)
        except Exception as e:
            print(f"Kimlik doğrulama hatası: {e}")
            return None

    def user_exists(self, username):
        """Kullanıcının var olup olmadığını kontrol et"""
        try:
            return self.model.user_exists(username)
        except Exception as e:
            print(f"Kullanıcı varlık kontrolü hatası: {e}")
            return False

    def create_user(self, username, password, is_admin=False):
        """Yeni kullanıcı oluştur"""
        try:
            return self.model.create_user(username, password, is_admin)
        except Exception as e:
            print(f"Kullanıcı oluşturma hatası: {e}")
            return False

    def update_user_login_stats(self, username):
        """Kullanıcının giriş istatistiklerini güncelle"""
        try:
            # Bu işlem authenticate metodunda otomatik olarak yapılıyor
            # Ekstra bir işlem gerekiyorsa buraya eklenebilir
            pass
        except Exception as e:
            print(f"Giriş istatistikleri güncelleme hatası: {e}")

    def get_all_users(self):
        """Tüm kullanıcıları al (admin işlemleri için)"""
        try:
            return self.model.get_all_users()
        except Exception as e:
            print(f"Tüm kullanıcıları alma hatası: {e}")
            return []

    def delete_user(self, user_id):
        """Kullanıcı sil (admin işlemleri için)"""
        try:
            return self.model.delete_user(user_id)
        except Exception as e:
            print(f"Kullanıcı silme hatası: {e}")
            return False, "Silme işlemi sırasında hata oluştu"

    def search_users(self, search_term):
        """Kullanıcılarda ara (admin işlemleri için)"""
        try:
            return self.model.search_users(search_term)
        except Exception as e:
            print(f"Kullanıcı arama hatası: {e}")
            return []

    def update_user_role(self, user_id, is_admin):
        """Kullanıcı rolünü güncelle (admin işlemleri için)"""
        try:
            return self.model.update_user_role(user_id, is_admin)
        except Exception as e:
            print(f"Kullanıcı rolü güncelleme hatası: {e}")
            return False, "Rol güncelleme sırasında hata oluştu"

    def get_user_by_id(self, user_id):
        """ID'ye göre kullanıcı al"""
        try:
            return self.model.get_user_by_id(user_id)
        except Exception as e:
            print(f"ID'ye göre kullanıcı alma hatası: {e}")
            return None

    def validate_user_credentials(self, username, password):
        """Kullanıcı kimlik bilgilerini doğrula"""
        try:
            if not username or not password:
                return False, "Kullanıcı adı ve şifre boş olamaz"
            
            if len(username) < 3:
                return False, "Kullanıcı adı en az 3 karakter olmalıdır"
            
            if len(password) < 4:
                return False, "Şifre en az 4 karakter olmalıdır"
            
            return True, "Geçerli kimlik bilgileri"
            
        except Exception as e:
            print(f"Kimlik bilgileri doğrulama hatası: {e}")
            return False, "Doğrulama sırasında hata oluştu"

    def get_current_user_info(self):
        """Mevcut kullanıcı bilgilerini al"""
        try:
            if hasattr(self.app_controller, 'current_user') and self.app_controller.current_user:
                return self.app_controller.current_user
            return None
        except Exception as e:
            print(f"Mevcut kullanıcı bilgisi alma hatası: {e}")
            return None

    def logout_user(self):
        """Kullanıcının çıkış işlemini gerçekleştir"""
        try:
            # AppController'da logout metodunu çağır
            if hasattr(self.app_controller, 'logout'):
                self.app_controller.logout()
            return True
        except Exception as e:
            print(f"Çıkış işlemi hatası: {e}")
            return False

    def is_admin_user(self, username):
        """Kullanıcının admin olup olmadığını kontrol et"""
        try:
            user = self.model.get_user_by_username(username)
            if user:
                return bool(user[5])  # is_admin column
            return False
        except Exception as e:
            print(f"Admin kontrolü hatası: {e}")
            return False

    def get_user_login_count(self, username):
        """Kullanıcının giriş sayısını al"""
        try:
            stats = self.model.get_user_stats(username)
            if stats:
                return stats[1]  # login_count
            return 0
        except Exception as e:
            print(f"Giriş sayısı alma hatası: {e}")
            return 0

    def get_user_last_login(self, username):
        """Kullanıcının son giriş zamanını al"""
        try:
            stats = self.model.get_user_stats(username)
            if stats:
                return stats[0]  # last_login
            return None
        except Exception as e:
            print(f"Son giriş zamanı alma hatası: {e}")
            return None

    def __del__(self):
        """Destructor"""
        try:
            # Cleanup işlemleri
            pass
        except:
            pass