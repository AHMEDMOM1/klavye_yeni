# controllers/login_controller.py
from keyboard_sound_app.models.user_model import UserModel
from keyboard_sound_app.views.admin_dashboard import AdminDashboard
from keyboard_sound_app.views.user_dashboard import UserDashboard

class LoginController:
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel()
        
    def login(self, username, password):
        auth_result = self.user_model.authenticate(username, password)
        if auth_result:
            # Giriş arayüzünü gizle
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Uygun kontrol panelini aç
            if auth_result["is_admin"]:
                AdminDashboard(self.root, self.user_model)
            else:
                UserDashboard(self.root)
            return True
        return False