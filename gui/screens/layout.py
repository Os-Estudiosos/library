from gui.screens import Screen
import customtkinter as ctk
from PIL import Image
import os
from config.colors import Colors


class Layout(Screen):
    def __init__(self, app):
        self.app = app

        self.options = [
            {
                "label": "Home",
                "route": "home",
                "callback": lambda: print("Mudando para Home")
            },
            {
                "label": "Livros",
                "route": "books",
                "callback": lambda: print("Mudando para Livros")
            },
            {
                "label": "Login",
                "route": "login",
                "callback": lambda: print("Mudando para Login")
            }
        ]

    def build(self, *args, **kwargs):
        image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "gui", "images", "icon.png")),
            size=(50,50)
        )
        image_label = ctk.CTkLabel(self.app, image=image, text="")
        image_label.grid(row=0, column=0, padx=20, pady=20)

        buttons_frame = ctk.CTkFrame(
            self.app,
            fg_color="#ffffff"
        )
        buttons_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ns")

        for i, option in enumerate(self.options):
            btn = ctk.CTkButton(
                buttons_frame,
                text=option["label"],
                command=option["callback"],
                font=("Arial", 14, "bold"),
                fg_color=Colors.INDIGO.c_600,
                hover_color=Colors.INDIGO.c_800
            )
            btn.grid(row=i+1, column=0, padx=10, pady=5, ipadx=5, ipady=5)
        
        frame = ctk.CTkScrollableFrame(
            self.app,
            corner_radius=5,
            fg_color=Colors.SLATE.c_200
        )

        frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
