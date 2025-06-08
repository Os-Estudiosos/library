from gui.screens import Screen
import customtkinter as ctk
from PIL import Image
import os
from config.colors import Colors


class Layout(Screen):
    def __init__(self, app):
        self.app = app

        def btn_callback(route):
            self.app.go_to(route)

        self.options = [
            {
                "label": "Estudantes",
                "route": "students",
                "callback": lambda: btn_callback("students")
            },
            {
                "label": "Livros",
                "route": "books",
                "callback": lambda: btn_callback("books")
            },
            {
                "label": "Atendentes",
                "route": "secretaries",
                "callback": lambda: btn_callback("secretaries")
            },
            {
                "label": "Categorias",
                "route": "categories",
                "callback": lambda: btn_callback("categories")
            },
            {
                "label": "Emprestimos",
                "route": "loans",
                "callback": lambda: btn_callback("loans")
            },
            {
                "label": "Grupos",
                "route": "groups",
                "callback": lambda: btn_callback("groups")
            },
            {
                "label": "Reservas",
                "route": "reserves",
                "callback": lambda: btn_callback("reserves")
            },
            {
                "label": "Suspensao",
                "route": "suspensions",
                "callback": lambda: btn_callback("suspensions")
            },
            {
                "label": "Turma",
                "route": "classes",
                "callback": lambda: btn_callback("classes")
            },
        ]

        self.frame = ctk.CTkScrollableFrame(
            self.app,
            corner_radius=5,
            fg_color=Colors.SLATE.c_200
        )
        self.frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

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
            state = "normal"
            color = "#fff"
            text_color = Colors.INDIGO.c_700
            if option["route"] == self.app.active:
                state = "disabled"
                color = Colors.INDIGO.c_800

            btn = ctk.CTkButton(
                buttons_frame,
                state=state,
                text=option["label"],
                text_color_disabled="#fff",
                fg_color=color,
                hover_color=Colors.PURPLE.c_200,
                text_color=text_color,
                command=option["callback"],
                font=("Arial", 14, "bold"),
            )
            btn.grid(row=i+1, column=0, padx=10, pady=5, ipadx=5, ipady=5)
    
    def restart(self):
        for i in self.frame.winfo_children():
            i.destroy()
