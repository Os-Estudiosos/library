from gui.screens import Screen
import customtkinter as ctk


class Login(Screen):
    def __init__(self, app):
        self.app = app
    
    def build(self, *args, **kwargs):
        def button_callback():
            self.app.go_back()

        button = ctk.CTkButton(self.app, text="Go Back", command=button_callback)
        button.grid(row=0, column=0, padx=20, pady=20)
