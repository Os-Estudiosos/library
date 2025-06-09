from gui.screens import Screen
import customtkinter as ctk
from config.colors import Colors
import pandas as pd
import tkinter as tk

from gui.manager.routemanager import RouteManager
from gui.screens.components.table import Table
from gui.screens.components.input import Input


class Reserves(Screen):
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
            text="Reservas",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Lista com todos as reservas registradas na livraria",
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
            command=lambda: RouteManager.go_to("create_reserve"),
            width=100,
            text_color="#fff",
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

        reserves = pd.read_csv("gui/screens/csv/reserves.csv")

        table = Table(self.app, "edit_reserves")

        pagination = {
            "registros": reserves.head(10),
            "total_registros": 40,
            "registros_por_pagina": 10,
            "total_paginas": 4,
            "pagina_atual": 1
        }

        table.build(pagination)


class EditReserve(Screen):
    def __init__(self, app):
        self.app = app

        self.form_dict = {
            "datares": {
                "label": "Data da Reserva:",
                "intype": "entry",
                "placeholder": "Ex: 20-03-2021"
            },
            "matriculaal": {
                "label": "Aluno:",
                "intype": "options",
            },
            "isbnliv": {
                "label": "Livro:",
                "intype": "options",
            },
        }

        self.student_dict = {
            "datares": tk.StringVar(),
            "matriculaal": tk.StringVar(),
            "isbnliv": tk.StringVar(),
        }

        self.layout = [
            ["datares", None],
            ["matriculaal", "isbnliv"]
        ]

        self.inputs=[]

    def send(self):
        RouteManager.go_back()
    
    def build(self, *args, **kwargs):
        reserve = args[0]

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
            text=f"Editar Reserva",
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

        forms_frame = ctk.CTkFrame(
            master=self.app,
            fg_color="#ffffff"
        )
        forms_frame.grid(row=1, column=0, sticky="nswe", padx=10)

        for i, line in enumerate(self.layout):
            for j, key in enumerate(line):
                if key is not None and self.form_dict[key]["intype"] == "entry":
                    forms_frame.rowconfigure(i, weight=1)
                    forms_frame.columnconfigure(j, weight=1)

                    wrapper = ctk.CTkFrame(
                        forms_frame,
                        fg_color="transparent"
                    )
                    wrapper.rowconfigure(0, weight=1)
                    wrapper.rowconfigure(1, weight=1)

                    label = ctk.CTkLabel(
                        wrapper,
                        text=self.form_dict[key]["label"],
                        text_color=Colors.GRAY.c_600
                    )
                    label.grid(row=0, column=0, sticky="w")

                    input = Input(
                        master=wrapper,
                        name=key,
                        placeholder_text=self.form_dict[key]["placeholder"],
                        border_width=1,
                        width=450,
                    )
                    input.grid(row=1, column=0, sticky="ew")
                    input.insert(0, reserve[key])

                    wrapper.grid(row=i, column=j, padx=10, pady=(10, 0), sticky="ew")

        confirm_button = ctk.CTkButton(
            forms_frame,
            text="Confirmar",
            font=("Arial", 14, "bold"),
            fg_color=Colors.INDIGO.c_600,
            hover_color=Colors.INDIGO.c_700,
            command=self.send,
            text_color="#fff",
            width=100,
            corner_radius=10
        )
        confirm_button.grid(row=i+1, column=0, ipady=5, sticky="w", padx=10, pady=(10, 10))


class CreateReserve(Screen):
    def __init__(self, app):
        self.app = app

        self.form_dict = {
            "datares": {
                "label": "Data da Reserva:",
                "intype": "entry",
                "placeholder": "Ex: 20-03-2021"
            },
            "matriculaal": {
                "label": "Aluno:",
                "intype": "options",
            },
            "isbnliv": {
                "label": "Livro:",
                "intype": "options",
            },
        }

        self.student_dict = {
            "datares": tk.StringVar(),
            "matriculaal": tk.StringVar(),
            "isbnliv": tk.StringVar(),
        }

        self.layout = [
            ["datares", None],
            ["matriculaal", "isbnliv"]
        ]

        self.inputs=[]

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
            text="Criar Reserva",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Você vai criar um registro de uma reserva, insira as informações e clique em INSERIR",
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


        forms_frame = ctk.CTkFrame(
            master=self.app,
            fg_color="#ffffff"
        )
        forms_frame.grid(row=1, column=0, sticky="nswe", padx=10)

        for i, line in enumerate(self.layout):
            for j, key in enumerate(line):
                if key is not None and self.form_dict[key]["intype"] == "entry":
                    forms_frame.rowconfigure(i, weight=1)
                    forms_frame.columnconfigure(j, weight=1)

                    wrapper = ctk.CTkFrame(
                        forms_frame,
                        fg_color="transparent"
                    )
                    wrapper.rowconfigure(0, weight=1)
                    wrapper.rowconfigure(1, weight=1)

                    label = ctk.CTkLabel(
                        wrapper,
                        text=self.form_dict[key]["label"],
                        text_color=Colors.GRAY.c_600
                    )
                    label.grid(row=0, column=0, sticky="w")

                    input = Input(
                        master=wrapper,
                        name=key,
                        placeholder_text=self.form_dict[key]["placeholder"],
                        border_width=1,
                        width=450,
                    )
                    input.grid(row=1, column=0, sticky="ew")

                    wrapper.grid(row=i, column=j, padx=10, pady=(10, 0), sticky="ew")

        confirm_button = ctk.CTkButton(
            forms_frame,
            text="Inserir",
            font=("Arial", 14, "bold"),
            fg_color=Colors.INDIGO.c_600,
            hover_color=Colors.INDIGO.c_700,
            command=self.send,
            text_color="#fff",
            width=100,
            corner_radius=10
        )
        confirm_button.grid(row=i+1, column=0, ipady=5, sticky="w", padx=10, pady=(10, 10))
