import sys
import os

# Proje yolunu ekliyoruz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keyboard_sound_app.controllers.app_controller import AppController

if __name__ == "__main__":
    AppController()