from gui.screens import Screen
import customtkinter as ctk
from config.colors import Colors
import pandas as pd
import tkinter as tk

from gui.manager.routemanager import RouteManager
from gui.screens.components.table import Table
from gui.screens.components.forms import Form

from gui.manager.tablesmanager import TablesManager


class Loans(Screen):
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
            text="Empréstimos",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Lista com todos os empréstimos registrados na livraria",
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
            command=lambda: RouteManager.go_to("create_loan"),
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

        pagination = TablesManager.emprestimoTable.read(qtd=self.items_per_page, pagina=page)

        table = Table(self.app, "edit_loans", TablesManager.emprestimoTable, ("idemp", "matriculaal"))
        table.build(pagination)


class EditLoan(Screen):
    def __init__(self, app):
        self.app = app
        self.current_idemp = None
        self.current_matriculaal = None
    
    def build(self, **kwargs):
        self.current_idemp = kwargs["entry"]["idemp"]
        self.current_matriculaal = kwargs["entry"]["matriculaal"]
        loan = TablesManager.emprestimoTable.read_one(
            idemp=self.current_idemp,
            matriculaal=self.current_matriculaal
        )

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
            text=f"Editar Empréstimo",
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
                "datainicioemp": {
                    "label": "Data de Início:",
                    "intype": "entry",
                    "placeholder": "Ex: 30-03-2018"
                },
                "datafimemp": {
                    "label": "Data de Fim:",
                    "intype": "entry",
                    "placeholder": "Ex: 30-03-2018"
                },
                "baixaemp": {
                    "label": "Baixa no Empréstimo:",
                    "intype": "toggle",
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
                "cpfatt": {
                    "label": "Atendente:",
                    "intype": "search",
                    "table": TablesManager.atendenteTable,
                    "exihibition_column": "primeironomeatt",
                    "value_column": "cpfatt"
                },
            },
            entry_dict={
                "datainicioemp": tk.StringVar(),
                "datafimemp": tk.StringVar(),
                "baixaemp": tk.StringVar(),
                "matriculaal": tk.StringVar(),
                "isbnliv": tk.StringVar(),
                "cpfatt": tk.StringVar(),
            },
            layout=[
                ["datainicioemp", "datafimemp"],
                ["baixaemp", "matriculaal"],
                ["isbnliv", "cpfatt"]
            ]
        )
        self.forms.build(self.send, loan)
    
    def send(self):
        values = self.forms.get_values()
        TablesManager.emprestimoTable.update({
            "idemp": self.current_idemp,
            "matriculaal": self.current_matriculaal,
        },values)
        RouteManager.go_back() 


class CreateLoan(Screen):
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
            text="Criar Empréstimo",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Você vai criar um registro de um empréstimo, insira as informações e clique em INSERIR",
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

        self.forms = Form(
            master=self.app,
            form_dict={
                "datainicioemp": {
                    "label": "Data de Início:",
                    "intype": "entry",
                    "placeholder": "Ex: 30-03-2018"
                },
                "datafimemp": {
                    "label": "Data de Fim:",
                    "intype": "entry",
                    "placeholder": "Ex: 30-03-2018"
                },
                "baixaemp": {
                    "label": "Baixa no Empréstimo:",
                    "intype": "toggle",
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
                "cpfatt": {
                    "label": "Atendente:",
                    "intype": "search",
                    "table": TablesManager.atendenteTable,
                    "exihibition_column": "primeironomeatt",
                    "value_column": "cpfatt"
                },
            },
            entry_dict={
                "datainicioemp": tk.StringVar(),
                "datafimemp": tk.StringVar(),
                "baixaemp": tk.StringVar(),
                "matriculaal": tk.StringVar(),
                "isbnliv": tk.StringVar(),
                "cpfatt": tk.StringVar(),
            },
            layout=[
                ["datainicioemp", "datafimemp"],
                ["baixaemp", "matriculaal"],
                ["isbnliv", "cpfatt"]
            ]
        )
        self.forms.build(self.send)
    
    def send(self):
        values = self.forms.get_values()
        new_values = values.copy()
        del new_values["matriculaal"]
        current_idres = TablesManager.emprestimoTable.read()["total_registros"]
        TablesManager.emprestimoTable.create({
            "idemp": current_idres+1,
            "matriculaal": values["matriculaal"],
        },new_values)
        RouteManager.go_back()
