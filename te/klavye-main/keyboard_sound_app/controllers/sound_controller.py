import pygame
from keyboard_sound_app.models.sound_model import SoundModel

class SoundController:
    def __init__(self, app_controller):
        self.app_controller = app_controller
        self.model = SoundModel()
        pygame.init()
        self.current_sound = None

    def load_sound(self, file_path):
        try:
            self.current_sound = pygame.mixer.Sound(file_path)
            return True
        except Exception as e:
            print(f"Ses yüklenirken hata: {e}")
            return False

    def play_sound(self):
        if self.current_sound:
            self.current_sound.play()

    def stop_sound(self):
        pygame.mixer.stop()

    def save_settings(self, user_id, file_path, volume=1.0):
        if self.load_sound(file_path):
            self.model.save_sound_setting(user_id, file_path, volume)
            return True
        return False

    def get_settings(self, user_id):
        return self.model.get_sound_setting(user_id)