from gui.screens import Screen
import customtkinter as ctk
from config.colors import Colors
import pandas as pd
import tkinter as tk

from gui.manager.routemanager import RouteManager
from gui.screens.components.table import Table
from gui.screens.components.forms import Form


class Secretaries(Screen):
    def __init__(self, app):
        self.app = app

    def build(self, *args, **kwargs):
        title_frame = ctk.CTkFrame(
            self.app,
            fg_color="transparent"
        )
        title_frame.rowconfigure(0, weight=1)
        title_frame.rowconfigure(1, weight=1)
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            title_frame,
            text="Atendentes",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Lista com todos os atendentes registrados na livraria",
            font=("Arial", 15, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        description.grid(column=0, row=1, sticky="w")

        buttons_frame = ctk.CTkFrame(
            title_frame,
            fg_color="transparent"
        )
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.rowconfigure(0, weight=1)

        add_button = ctk.CTkButton(
            buttons_frame,
            text="Adicionar",
            font=("Arial", 14, "bold"),
            fg_color=Colors.INDIGO.c_600,
            hover_color=Colors.INDIGO.c_700,
            text_color="#fff",
            command=lambda: RouteManager.go_to("create_att"),
            width=100,
            corner_radius=10
        )
        add_button.grid(column=0, row=0, ipady=5, padx=(0, 10), sticky="e")

        cancel_button = ctk.CTkButton(
            buttons_frame,
            command=lambda: print("Filtro"),
            fg_color="#ffffff",
            hover_color=Colors.GRAY.c_100,
            text_color=Colors.GRAY.c_800,
            border_color=Colors.GRAY.c_300,
            border_width=1,
            text="Filtro",
            font=("Arial", 13, "bold"),
            width=100,
            corner_radius=10
        )
        cancel_button.grid(column=1, row=0, ipady=5)

        buttons_frame.grid(column=1, row=0, rowspan=2, sticky="nsew")

        title_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        atts = pd.read_csv("gui/screens/csv/atts.csv")

        table = Table(self.app, "edit_atts")

        pagination = {
            "registros": atts,
            "total_registros": 8,
            "registros_por_pagina": 8,
            "total_paginas": 1,
            "pagina_atual": 1
        }

        table.build(pagination)


class EditSecretary(Screen):
    def __init__(self, app):
        self.app = app

    def send(self):
        RouteManager.go_back()
    
    def build(self, *args, **kwargs):
        att = args[0]

        title_frame = ctk.CTkFrame(
            self.app,
            fg_color="transparent"
        )
        title_frame.rowconfigure(0, weight=1)
        title_frame.rowconfigure(1, weight=1)
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            title_frame,
            text=f"Editar {att.primeironomeatt} {att.ultimonomeatt}",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Edite os campos e clique em EDITAR para alterar o registro",
            font=("Arial", 15, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        description.grid(column=0, row=1, sticky="w")

        cancel_button = ctk.CTkButton(
            title_frame,
            command=lambda: RouteManager.go_back(),
            fg_color="#ffffff",
            hover_color=Colors.GRAY.c_100,
            text_color=Colors.GRAY.c_800,
            border_color=Colors.GRAY.c_300,
            border_width=1,
            text="Cancelar",
            font=("Arial", 13, "bold"),
            width=100,
            corner_radius=10
        )
        cancel_button.grid(column=1, row=0, ipady=5, rowspan=2, sticky="e")

        title_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        self.forms = Form(
            master=self.app,
            form_dict={
                "cpfatt": {
                    "label": "CPF:",
                    "intype": "entry",
                    "placeholder": "Ex: 0392839"
                },
                "primeironomeatt": {
                    "label": "Primeiro Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: Carlos"
                },
                "ultimonomeatt": {
                    "label": "Último Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: Alberto"
                },
            },
            entry_dict={
                "cpfatt": tk.StringVar(),
                "primeironomeatt": tk.StringVar(),
                "ultimonomeatt": tk.StringVar(),
            },
            layout=[
                ["cpfatt"],
                ["primeironomeatt"],
                ["ultimonomeatt"]
            ]
        )
        self.forms.build(self.send, att)


class CreateSecretary(Screen):
    def __init__(self, app):
        self.app = app

    def send(self):
        RouteManager.go_back()
    
    def build(self, *args, **kwargs):
        title_frame = ctk.CTkFrame(
            self.app,
            fg_color="transparent"
        )
        title_frame.rowconfigure(0, weight=1)
        title_frame.rowconfigure(1, weight=1)
        title_frame.columnconfigure(0, weight=1)
        title_frame.columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            title_frame,
            text="Criar Atendente",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Você vai criar um registro de um atendente, insira as informações e clique em INSERIR",
            font=("Arial", 15, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        description.grid(column=0, row=1, sticky="w")

        cancel_button = ctk.CTkButton(
            title_frame,
            command=lambda: RouteManager.go_back(),
            fg_color="#ffffff",
            hover_color=Colors.GRAY.c_100,
            text_color=Colors.GRAY.c_800,
            border_color=Colors.GRAY.c_300,
            border_width=1,
            text="Cancelar",
            font=("Arial", 13, "bold"),
            width=100,
            corner_radius=10
        )
        cancel_button.grid(column=1, row=0, ipady=5, rowspan=2, sticky="e")

        title_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        self.forms = Form(
            master=self.app,
            form_dict={
                "cpfatt": {
                    "label": "CPF:",
                    "intype": "entry",
                    "placeholder": "Ex: 0392839"
                },
                "primeironomeatt": {
                    "label": "Primeiro Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: Carlos"
                },
                "ultimonomeatt": {
                    "label": "Último Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: Alberto"
                },
            },
            entry_dict={
                "cpfatt": tk.StringVar(),
                "primeironomeatt": tk.StringVar(),
                "ultimonomeatt": tk.StringVar(),
            },
            layout=[
                ["cpfatt"],
                ["primeironomeatt"],
                ["ultimonomeatt"]
            ]
        )
        self.forms.build(self.send)
