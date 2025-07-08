import tkinter as tk
from tkinter import ttk

class Styles:
    def __init__(self):
        self.style = ttk.Style()
        self.setup_styles()

    def setup_styles(self):
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f5f6f7')
        self.style.configure('TLabel', background='#f5f6f7', foreground='#333', font=('Segoe UI', 10))
        self.style.configure('TButton', 
                          font=('Segoe UI', 10, 'bold'), 
                          borderwidth=1, 
                          relief='flat',
                          foreground='white',
                          background='#4a6da7')
        self.style.map('TButton', background=[('active', '#3a5a8f')])
        self.style.configure('TEntry', fieldbackground='white', borderwidth=1)
        self.style.configure('TCombobox', fieldbackground='white', borderwidth=1)
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        self.style.configure('Accent.TButton', background='#2ecc71')
        self.style.map('Accent.TButton', background=[('active', '#27ae60')])
        self.style.configure('Danger.TButton', background='#e74c3c')
        self.style.map('Danger.TButton', background=[('active', '#c0392b')])