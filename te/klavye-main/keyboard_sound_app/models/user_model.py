# user_model.py
import sqlite3
from datetime import datetime
from keyboard_sound_app.utils.database import Database

class UserModel:
    def __init__(self):
        self.db = Database()
        self.create_table()
        self.add_admin_user()  

    def create_table(self):
        """Kullanıcılar tablosunu oluştur"""
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            last_login DATETIME,
            login_count INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0
        )
        """
        self.db.execute(query)

    def add_admin_user(self):
        """Varsayılan yönetici kullanıcı yoksa ekle"""
        if not self.get_user_by_username("Admin123"):
            self.create_user("Admin123", "Admin123", is_admin=True)

    def create_user(self, username, password, is_admin=False):
        """Yeni kullanıcı oluştur"""
        query = "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)"
        try:
            self.db.execute(query, (username, password, 1 if is_admin else 0))
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.Error as e:
            print(f"Kullanıcı oluşturulurken hata oluştu: {e}")
            return False

    def authenticate(self, username, password):
        """Kullanıcının kimliğini doğrula"""
        query = "SELECT id, password, is_admin FROM users WHERE username = ?"
        result = self.db.fetch_one(query, (username,))
        
        if result and result[1] == password:
            user_id = result[0]
            # Son giriş tarihini ve giriş sayısını güncelle
            update_query = """
            UPDATE users 
            SET last_login = ?, login_count = login_count + 1 
            WHERE id = ?
            """
            try:
                self.db.execute(update_query, (datetime.now(), user_id))
            except sqlite3.Error as e:
                print(f"Giriş bilgileri güncellenirken hata oluştu: {e}")
            
            return {
                "id": user_id,
                "username": username,
                "is_admin": bool(result[2])
            }
        return None

    def get_user_stats(self, username):
        """Kullanıcı istatistiklerini al"""
        query = "SELECT last_login, login_count FROM users WHERE username = ?"
        return self.db.fetch_one(query, (username,))

    def get_all_users(self):
        """Tüm kullanıcıları detaylarıyla al - created_at olmadan"""
        query = """
        SELECT id, username, last_login, login_count, is_admin 
        FROM users 
        ORDER BY id DESC
        """
        return self.db.fetch_all(query)

    def get_user_by_username(self, username):
        """Kullanıcı adıyla kullanıcıyı al"""
        query = "SELECT * FROM users WHERE username = ?"
        return self.db.fetch_one(query, (username,))
    
    def get_user_by_id(self, user_id):
        """ID ile kullanıcıyı al"""
        query = "SELECT * FROM users WHERE id = ?"
        return self.db.fetch_one(query, (user_id,))

    def delete_user(self, user_id):
        """Kullanıcı sil (ana yöneticinin silinmesine karşı koruma yap)"""
        # Kullanıcının ana yönetici olup olmadığını kontrol et
        user = self.get_user_by_id(user_id)
        if user and user[1] == "Admin123":  # username ikinci sütundur
            return False, "Ana yönetici silinemez"
        
        query = "DELETE FROM users WHERE id = ? AND id != (SELECT id FROM users WHERE username = 'Admin123')"
        try:
            result = self.db.execute(query, (user_id,))
            if result:
                return True, "Kullanıcı başarıyla silindi"
            return False, "Kullanıcı silinemedi"
        except sqlite3.Error as e:
            print(f"Kullanıcı silinirken hata oluştu: {e}")
            return False, "Veritabanı hatası"

    def search_users(self, search_term):
        """Kullanıcılarda ara - created_at olmadan"""
        query = """
        SELECT id, username, last_login, login_count, is_admin 
        FROM users 
        WHERE username LIKE ? 
        ORDER BY id DESC
        """
        try:
            return self.db.fetch_all(query, (f'%{search_term}%',))
        except sqlite3.Error as e:
            print(f"Arama sırasında hata oluştu: {e}")
            return []
    
    def update_user_role(self, user_id, is_admin):
        """Kullanıcının rolünü güncelle"""
        # Kullanıcının ana yönetici olup olmadığını kontrol et
        user = self.get_user_by_id(user_id)
        if user and user[1] == "Admin123":  # username ikinci sütundur
            return False, "Ana yöneticinin rolü değiştirilemez"
        
        query = "UPDATE users SET is_admin = ? WHERE id = ?"
        try:
            self.db.execute(query, (1 if is_admin else 0, user_id))
            return True, "Yetkiler başarıyla güncellendi"
        except sqlite3.Error as e:
            print(f"Yetki güncellenirken hata oluştu: {e}")
            return False, "Veritabanı hatası"

    def user_exists(self, username):
        """Kullanıcının varlığını kontrol et"""
        user = self.get_user_by_username(username)
        return user is not None

    def get_users_count(self):
        """Kullanıcı sayısını al"""
        query = "SELECT COUNT(*) FROM users"
        result = self.db.fetch_one(query)
        return result[0] if result else 0

    def get_admin_users(self):
        """Sadece yönetici kullanıcıları al - created_at olmadan"""
        query = """
        SELECT id, username, last_login, login_count, is_admin 
        FROM users 
        WHERE is_admin = 1 
        ORDER BY id DESC
        """
        return self.db.fetch_all(query)

    def get_regular_users(self):
        """Sadece normal kullanıcıları al - created_at olmadan"""
        query = """
        SELECT id, username, last_login, login_count, is_admin 
        FROM users 
        WHERE is_admin = 0 
        ORDER BY id DESC
        """
        return self.db.fetch_all(query)

    def update_user_password(self, user_id, new_password):
        """Kullanıcının şifresini güncelle"""
        query = "UPDATE users SET password = ? WHERE id = ?"
        try:
            self.db.execute(query, (new_password, user_id))
            return True, "Şifre başarıyla güncellendi"
        except sqlite3.Error as e:
            print(f"Şifre güncellenirken hata oluştu: {e}")
            return False, "Veritabanı hatası"

    def get_user_login_history(self, user_id):
        """Kullanıcının giriş geçmişini al - created_at olmadan"""
        query = """
        SELECT username, last_login, login_count 
        FROM users 
        WHERE id = ?
        """
        return self.db.fetch_one(query, (user_id,))

    def validate_username(self, username):
        """Kullanıcı adını doğrula"""
        if not username:
            return False, "Kullanıcı adı boş olamaz"
        
        if len(username) < 3:
            return False, "Kullanıcı adı en az 3 karakter olmalıdır"
        
        if len(username) > 50:
            return False, "Kullanıcı adı en fazla 50 karakter olabilir"
        
        # Özel karakter kontrolü
        import re
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "Kullanıcı adı sadece harf, rakam ve alt çizgi içerebilir"
        
        return True, "Geçerli kullanıcı adı"

    def validate_password(self, password):
        """Şifreyi doğrula"""
        if not password:
            return False, "Şifre boş olamaz"
        
        if len(password) < 4:
            return False, "Şifre en az 4 karakter olmalıdır"
        
        if len(password) > 100:
            return False, "Şifre en fazla 100 karakter olabilir"
        
        return True, "Geçerli şifre"

    def get_total_login_count(self):
        """Toplam giriş sayısını al"""
        query = "SELECT SUM(login_count) FROM users"
        result = self.db.fetch_one(query)
        return result[0] if result and result[0] else 0

    def get_active_users_count(self):
        """En az bir kez giriş yapmış kullanıcı sayısını al"""
        query = "SELECT COUNT(*) FROM users WHERE login_count > 0"
        result = self.db.fetch_one(query)
        return result[0] if result else 0

    def get_never_logged_in_users(self):
        """Hiç giriş yapmamış kullanıcıları al"""
        query = """
        SELECT id, username, is_admin 
        FROM users 
        WHERE login_count = 0 OR last_login IS NULL
        ORDER BY id DESC
        """
        return self.db.fetch_all(query)

    def get_most_active_users(self, limit=5):
        """En aktif kullanıcıları al"""
        query = """
        SELECT id, username, login_count, last_login, is_admin 
        FROM users 
        WHERE login_count > 0 
        ORDER BY login_count DESC 
        LIMIT ?
        """
        return self.db.fetch_all(query, (limit,))

    def reset_user_login_count(self, user_id):
        """Kullanıcının giriş sayısını sıfırla"""
        query = "UPDATE users SET login_count = 0 WHERE id = ?"
        try:
            self.db.execute(query, (user_id,))
            return True, "Giriş sayısı sıfırlandı"
        except sqlite3.Error as e:
            print(f"Giriş sayısı sıfırlanırken hata oluştu: {e}")
            return False, "Veritabanı hatası"

    def update_last_login(self, user_id):
        """Son giriş tarihini güncelle"""
        query = "UPDATE users SET last_login = ? WHERE id = ?"
        try:
            self.db.execute(query, (datetime.now(), user_id))
            return True
        except sqlite3.Error as e:
            print(f"Son giriş tarihi güncellenirken hata oluştu: {e}")
            return False

    def get_database_info(self):
        """Veritabanı bilgilerini al"""
        try:
            cursor = self.db.connection.cursor()
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            
            return {
                "table_name": "users",
                "columns": columns,
                "total_users": self.get_users_count(),
                "admin_users": len(self.get_admin_users()),
                "regular_users": len(self.get_regular_users())
            }
        except Exception as e:
            print(f"Veritabanı bilgisi alınırken hata oluştu: {e}")
            return None

    def __del__(self):
        """Destructor"""
        try:
            # Cleanup işlemleri
            pass
        except:
            pass