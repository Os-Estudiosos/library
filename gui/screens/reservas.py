from gui.screens import Screen
import customtkinter as ctk
from config.colors import Colors
import pandas as pd
import tkinter as tk

from gui.manager.routemanager import RouteManager
from gui.screens.components.table import Table
from gui.screens.components.forms import Form
from gui.screens.components.empty import EmptyFrame

from gui.manager.tablesmanager import TablesManager


class Reserves(Screen):
    def __init__(self, app):
        self.app = app
        self.items_per_page = 10

    def build(self, **kwargs):
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

        if "page" in kwargs.keys():
            page = kwargs["page"]
        else:
            page = 1

        pagination = TablesManager.reservaTable.read(qtd=self.items_per_page, pagina=page)
        
        if pagination:
            table = Table(self.app, "edit_reserves", TablesManager.reservaTable, ("idres", "matriculaal"))
            table.build(pagination)
        else:
            empty_frame = EmptyFrame(self.app)
            empty_frame.build()


class EditReserve(Screen):
    def __init__(self, app):
        self.app = app

        self.current_idres = None
        self.current_matriculaal = None
    
    def build(self, **kwargs):
        self.current_idres = kwargs["entry"]["idres"]
        self.current_matriculaal = kwargs["entry"]["matriculaal"]
        reserve = TablesManager.reservaTable.read_one(
            idres=self.current_idres,
            matriculaal=self.current_matriculaal
        )

        print(reserve)

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

        self.forms = Form(
            master=self.app,
            form_dict={
                "datares": {
                    "label": "Data da Reserva:",
                    "intype": "entry",
                    "placeholder": "Ex: 20-03-2021"
                },
                "matriculaal": {
                    "label": "Aluno:",
                    "intype": "search",
                    "table": TablesManager.alunoTable,
                    "exihibition_column": "primeironomeal",
                    "value_column": "matriculaal"
                },
                "isbnliv": {
                    "label": "Livro:",
                    "intype": "search",
                    "table": TablesManager.livroTable,
                    "exihibition_column": "nomeliv",
                    "value_column": "isbnliv"
                },
            },
            entry_dict={
                "datares": tk.StringVar(),
                "matriculaal": tk.StringVar(),
                "isbnliv": tk.StringVar(),
            },
            layout=[
                ["datares"],
                ["matriculaal"],
                ["isbnliv"]
            ]
        )
        self.forms.build(self.send, reserve)

    def send(self):
        values = self.forms.get_values()
        TablesManager.reservaTable.update({
            "idres": self.current_idres,
            "matriculaal": self.current_matriculaal,
        },values)
        RouteManager.go_back() 


class CreateReserve(Screen):
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

        self.forms = Form(
            master=self.app,
            form_dict={
                "datares": {
                    "label": "Data da Reserva:",
                    "intype": "entry",
                    "placeholder": "Ex: 20-03-2021"
                },
                "matriculaal": {
                    "label": "Aluno:",
                    "intype": "search",
                    "table": TablesManager.alunoTable,
                    "exihibition_column": "primeironomeal",
                    "value_column": "matriculaal"
                },
                "isbnliv": {
                    "label": "Livro:",
                    "intype": "search",
                    "table": TablesManager.livroTable,
                    "exihibition_column": "nomeliv",
                    "value_column": "isbnliv"
                },
            },
            entry_dict={
                "datares": tk.StringVar(),
                "matriculaal": tk.StringVar(),
                "isbnliv": tk.StringVar(),
            },
            layout=[
                ["datares"],
                ["matriculaal"],
                ["isbnliv"]
            ]
        )
        self.forms.build(self.send)
    
    def send(self):
        values = self.forms.get_values()
        new_values = values.copy()
        del new_values["matriculaal"]
        current_idres = TablesManager.reservaTable.read()["total_registros"]
        TablesManager.reservaTable.create({
            "idres": current_idres+1,
            "matriculaal": values["matriculaal"],
        },new_values)
        RouteManager.go_back()
