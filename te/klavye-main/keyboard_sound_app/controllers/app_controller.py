# app_controller.py
import tkinter as tk
from pynput.keyboard import Listener
import threading
from keyboard_sound_app.controllers.user_controller import UserController
from keyboard_sound_app.controllers.sound_controller import SoundController
from keyboard_sound_app.controllers.admin_controller import AdminController
from keyboard_sound_app.views.login_view import LoginView
from keyboard_sound_app.views.main_view import MainView

class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Ana pencereyi gizle
        
        # Controller'ları başlat
        self.user_controller = UserController(self)
        self.sound_controller = None
        self.admin_controller = AdminController(self)
        
        # Mevcut kullanıcı bilgileri
        self.current_user = None
        self.current_admin = None
        
        # View'ları saklamak için
        self.login_view = None
        self.main_view = None
        
        # Keyboard listener
        self.keyboard_listener_thread = None
        self.keyboard_listener_active = False
        
        # Uygulamayı başlat
        self.show_login_window()
        self.start_keyboard_listener()
        
        # Ana döngü
        self.root.mainloop()

    def show_login_window(self):
        """Login penceresini göster"""
        try:
            # Mevcut view'ları temizle
            if hasattr(self, 'main_view') and self.main_view:
                self.main_view.destroy()
                self.main_view = None
            
            # Login window oluştur
            if self.login_view is None:
                login_window = tk.Toplevel(self.root)
                self.login_view = LoginView(login_window, self)
            else:
                self.login_view.window.deiconify()
                self.login_view.window.lift()
            
            # Ana pencereyi gizle
            self.root.withdraw()
            
        except Exception as e:
            print(f"Login penceresi gösterilirken hata: {e}")

    def show_main_application(self, user_data):
        """Ana uygulamayı göster"""
        try:
            self.current_user = user_data
            
            # Login view'ını gizle
            if self.login_view:
                self.login_view.root.withdraw()
            
            # Main view'ı oluştur
            main_window = tk.Toplevel(self.root)
            self.main_view = MainView(main_window, self)
            
            # Kullanıcı bilgilerini set et
            username = user_data.get('username', 'Bilinmiyor')
            user_stats = self.user_controller.model.get_user_stats(username)
            
            if user_stats:
                login_count = user_stats[1] if user_stats[1] else 0
                last_login = user_stats[0] if user_stats[0] else "Hiç giriş yapılmadı"
                self.main_view.set_user_info(username, login_count, last_login)
            
            # Sound controller'ı başlat
            self.sound_controller = SoundController(self)
            
            # Kaydedilmiş ses ayarlarını yükle
            settings = self.sound_controller.get_settings(user_data.get('id', 1))
            if settings:
                self.main_view.set_file_path(settings[0])
            
            # Keyboard listener'ı etkinleştir
            self.keyboard_listener_active = True
            
        except Exception as e:
            print(f"Ana uygulama gösterilirken hata: {e}")
            if self.login_view:
                self.login_view.show_error(f"Ana uygulama açılırken hata: {str(e)}")

    def show_admin_dashboard(self):
        """Admin dashboard'ı göster"""
        try:
            # Login view'ını gizle
            if self.login_view:
                self.login_view.root.withdraw()
            
            # Admin dashboard'ı göster
            self.admin_controller.show_admin_dashboard()
            
            # Keyboard listener'ı devre dışı bırak (admin panelinde gerekli değil)
            self.keyboard_listener_active = False
            
        except Exception as e:
            print(f"Admin dashboard gösterilirken hata: {e}")
            if self.login_view:
                self.login_view.show_error(f"Admin paneli açılırken hata: {str(e)}")

    def login(self, username, password):
        """Kullanıcı girişi"""
        try:
            # UserController üzerinden kimlik doğrulama
            auth_result = self.user_controller.login(username, password)
            
            if auth_result:
                user_data = auth_result
                self.current_user = user_data
                
                # Login başarılı, kullanıcı tipine göre yönlendir
                if user_data.get('is_admin'):
                    # Admin kullanıcı
                    self.current_admin = user_data
                    return True, user_data
                else:
                    # Normal kullanıcı
                    return True, user_data
            else:
                return False, None
                
        except Exception as e:
            print(f"Login hatası: {e}")
            return False, None

    def register(self, username, password, is_admin=False):
        """Kullanıcı kaydı"""
        try:
            success, message = self.user_controller.register(username, password, is_admin)
            return success, message
        except Exception as e:
            print(f"Kayıt hatası: {e}")
            return False, f"Kayıt sırasında hata: {str(e)}"

    def logout(self):
        """Çıkış yap"""
        try:
            # Mevcut kullanıcı bilgilerini temizle
            self.current_user = None
            self.current_admin = None
            
            # Sound controller'ı durdur
            if self.sound_controller:
                self.sound_controller.stop_sound()
                self.sound_controller = None
            
            # Keyboard listener'ı devre dışı bırak
            self.keyboard_listener_active = False
            
            # View'ları temizle
            if self.main_view:
                self.main_view.destroy()
                self.main_view = None
            
            # Admin dashboard'ı kapat
            if self.admin_controller:
                self.admin_controller.close_admin_dashboard()
            
            # Login penceresini göster
            self.show_login_window()
            
        except Exception as e:
            print(f"Çıkış yapılırken hata: {e}")

    def preview_sound(self, file_path):
        """Ses önizlemesi"""
        try:
            if file_path and self.sound_controller:
                if self.sound_controller.load_sound(file_path):
                    self.sound_controller.play_sound()
                    return True
            return False
        except Exception as e:
            print(f"Ses önizleme hatası: {e}")
            return False

    def stop_sound(self):
        """Sesi durdur"""
        try:
            if self.sound_controller:
                self.sound_controller.stop_sound()
        except Exception as e:
            print(f"Ses durdurma hatası: {e}")

    def save_settings(self, file_path):
        """Ses ayarlarını kaydet"""
        try:
            if file_path and self.current_user and self.sound_controller:
                user_id = self.current_user.get('id', 1)
                self.sound_controller.save_settings(user_id, file_path)
                return True
            return False
        except Exception as e:
            print(f"Ayar kaydetme hatası: {e}")
            return False

    def get_current_user(self):
        """Mevcut kullanıcıyı al"""
        return self.current_user

    def get_current_admin(self):
        """Mevcut admin kullanıcısını al"""
        return self.current_admin

    def is_admin_logged_in(self):
        """Admin girişi yapılmış mı?"""
        return self.current_admin is not None

    def is_user_logged_in(self):
        """Kullanıcı girişi yapılmış mı?"""
        return self.current_user is not None

    def get_user_stats(self, username):
        """Kullanıcı istatistiklerini al"""
        try:
            return self.user_controller.model.get_user_stats(username)
        except Exception as e:
            print(f"Kullanıcı istatistikleri alınırken hata: {e}")
            return None

    def update_user_stats(self, username):
        """Kullanıcı istatistiklerini güncelle"""
        try:
            # Bu metod login sırasında otomatik olarak çağrılıyor
            pass
        except Exception as e:
            print(f"Kullanıcı istatistikleri güncellenirken hata: {e}")

    def start_keyboard_listener(self):
        """Klavye dinleyicisini başlat"""
        def on_press(key):
            try:
                # Sadece ana uygulama açıkken ve ses ayarlandıysa çalışsın
                if (self.keyboard_listener_active and 
                    self.sound_controller and 
                    self.sound_controller.current_sound and
                    self.current_user and
                    not self.current_user.get('is_admin')):  # Admin modunda çalışmasın
                    
                    self.sound_controller.play_sound()
            except Exception as e:
                print(f"Klavye dinleyici hatası: {e}")

        def start_listener():
            try:
                self.keyboard_listener = Listener(on_press=on_press)
                self.keyboard_listener.start()
                self.keyboard_listener.join()
            except Exception as e:
                print(f"Klavye dinleyici başlatma hatası: {e}")

        if not self.keyboard_listener_thread or not self.keyboard_listener_thread.is_alive():
            self.keyboard_listener_thread = threading.Thread(
                target=start_listener,
                daemon=True
            )
            self.keyboard_listener_thread.start()

    def stop_keyboard_listener(self):
        """Klavye dinleyicisini durdur"""
        try:
            self.keyboard_listener_active = False
            if hasattr(self, 'keyboard_listener') and self.keyboard_listener:
                self.keyboard_listener.stop()
        except Exception as e:
            print(f"Klavye dinleyici durdurma hatası: {e}")

    def restart_keyboard_listener(self):
        """Klavye dinleyicisini yeniden başlat"""
        try:
            self.stop_keyboard_listener()
            self.start_keyboard_listener()
        except Exception as e:
            print(f"Klavye dinleyici yeniden başlatma hatası: {e}")

    def exit_app(self):
        """Uygulamayı kapat"""
        try:
            # Ses durdur
            self.stop_sound()
            
            # Klavye dinleyicisini durdur
            self.stop_keyboard_listener()
            
            # Admin dashboard'ı kapat
            if self.admin_controller:
                self.admin_controller.close_admin_dashboard()
            
            # View'ları temizle
            if self.main_view:
                self.main_view.destroy()
            
            if self.login_view:
                self.login_view.root.destroy()
            
            # Ana pencereyi kapat
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            print(f"Uygulama kapatılırken hata: {e}")
            # Zorla kapat
            import sys
            sys.exit(0)

    def minimize_all_windows(self):
        """Tüm pencereleri küçült"""
        try:
            if self.main_view:
                self.main_view.window.iconify()
            
            if self.login_view:
                self.login_view.root.iconify()
            
            if self.admin_controller and self.admin_controller.admin_dashboard:
                self.admin_controller.admin_dashboard.window.iconify()
                
        except Exception as e:
            print(f"Pencereler küçültülürken hata: {e}")

    def restore_all_windows(self):
        """Tüm pencereleri geri yükle"""
        try:
            if self.main_view:
                self.main_view.window.deiconify()
            
            if self.login_view:
                self.login_view.root.deiconify()
            
            if self.admin_controller and self.admin_controller.admin_dashboard:
                self.admin_controller.admin_dashboard.window.deiconify()
                
        except Exception as e:
            print(f"Pencereler geri yüklenirken hata: {e}")

    def get_app_version(self):
        """Uygulama versiyonunu al"""
        return "1.0.0"

    def get_app_name(self):
        """Uygulama adını al"""
        return "Klavye Ses Uygulaması"

    def get_app_info(self):
        """Uygulama bilgilerini al"""
        return {
            "name": self.get_app_name(),
            "version": self.get_app_version(),
            "current_user": self.current_user,
            "current_admin": self.current_admin,
            "keyboard_listener_active": self.keyboard_listener_active
        }

    def handle_exception(self, exception):
        """Genel exception handler"""
        print(f"Uygulama hatası: {exception}")
        # Gerekirse kullanıcıya bilgi ver
        try:
            if self.login_view:
                self.login_view.show_error(f"Sistem hatası: {str(exception)}")
        except:
            pass

    def reload_user_data(self):
        """Kullanıcı verilerini yeniden yükle"""
        try:
            if self.current_user:
                username = self.current_user.get('username')
                if username:
                    user_stats = self.get_user_stats(username)
                    if user_stats and self.main_view:
                        self.main_view.set_user_info(username, user_stats[1], user_stats[0])
        except Exception as e:
            print(f"Kullanıcı verileri yeniden yüklenirken hata: {e}")

    def check_admin_permissions(self):
        """Admin yetkilerini kontrol et"""
        return self.current_admin is not None or (
            self.current_user and self.current_user.get('is_admin', False)
        )

    def __del__(self):
        """Destructor"""
        try:
            self.stop_keyboard_listener()
            self.stop_sound()
        except:
            pass