from gui.screens import Screen
import customtkinter as ctk
import pandas as pd
from config.colors import Colors
import tkinter as tk

from gui.manager.routemanager import RouteManager

from gui.screens.components.table import Table
from gui.screens.components.input import Input, SearchSelect
from gui.screens.components.forms import Form

from gui.manager.tablesmanager import TablesManager


class Students(Screen):
    def __init__(self, app):
        self.app = app
        self.items_per_page = 10

    def build(self, *args, **kwargs):
        if args[0] is not None:
            page = args[0]
        else:
            page = 1
        
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
            text="Alunos",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Lista com todos os alunos registrados na livraria",
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
            text_color="#fff",
            font=("Arial", 14, "bold"),
            fg_color=Colors.INDIGO.c_600,
            hover_color=Colors.INDIGO.c_700,
            command=lambda: RouteManager.go_to("create_student"),
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

        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        pagination = TablesManager.alunoTable.read(qtd=self.items_per_page, pagina=page)

        table = Table(self.app, "edit_students", TablesManager.alunoTable, "matriculaal")
        table.build(pagination)


class EditStudent(Screen):
    def __init__(self, app):
        self.app = app

    def send(self):
        RouteManager.go_back()
    
    def build(self, *args, **kwargs):
        student = args[0]

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
            text=f"Editar {student.primeironomeal} {student.ultimonomeal}",
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
                "matriculaal": {
                    "label": "Matrícula:",
                    "intype": "entry",
                    "placeholder": "Ex: 0392839"
                },
                "primeironomeal": {
                    "label": "Primeiro Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: José"
                },
                "ultimonomeal": {
                    "label": "Último Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: Alberto"
                },
                "datanascimentoal": {
                    "label": "Data de Nascimento:",
                    "intype": "entry",
                    "placeholder": "Ex: 20-13-2005"
                },
                "senhaal": {
                    "label": "Senha do Aluno:",
                    "intype": "entry",
                    "placeholder": "Ex: axzoue!Lso$p028"
                },
                "idturma": {
                    "label": "Turma do Aluno:",
                    "intype": "search",
                    "table": "classes",
                    "exihibition_column": "nometurma",
                    "value_column": "idturma"
                }
            },
            entry_dict={
                "matriculaal": tk.StringVar(),
                "primeironomeal": tk.StringVar(),
                "ultimonomeal": tk.StringVar(),
                "datanascimentoal": tk.StringVar(),
                "senhaal": tk.StringVar(),
                "idturma": tk.StringVar()
            },
            layout=[
                ["matriculaal", "datanascimentoal"],
                ["primeironomeal", "ultimonomeal"],
                ["senhaal", "idturma"]
            ]
        )

        self.forms.build(self.send, student)


class CreateStudent(Screen):
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
            text="Criar Aluno",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Você vai criar um registro de aluno, insira as informações e clique em INSERIR",
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
                "matriculaal": {
                    "label": "Matrícula:",
                    "intype": "entry",
                    "placeholder": "Ex: 0392839"
                },
                "primeironomeal": {
                    "label": "Primeiro Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: José"
                },
                "ultimonomeal": {
                    "label": "Último Nome:",
                    "intype": "entry",
                    "placeholder": "Ex: Alberto"
                },
                "datanascimentoal": {
                    "label": "Data de Nascimento:",
                    "intype": "entry",
                    "placeholder": "Ex: 20-13-2005"
                },
                "senhaal": {
                    "label": "Senha do Aluno:",
                    "intype": "entry",
                    "placeholder": "Ex: axzoue!Lso$p028"
                },
                "idturma": {
                    "label": "Turma do Aluno:",
                    "intype": "search",
                    "table": "classes",
                    "exihibition_column": "nometurma",
                    "value_column": "idturma"
                }
            },
            entry_dict={
                "matriculaal": tk.StringVar(),
                "primeironomeal": tk.StringVar(),
                "ultimonomeal": tk.StringVar(),
                "datanascimentoal": tk.StringVar(),
                "senhaal": tk.StringVar(),
                "idturma": tk.StringVar()
            },
            layout=[
                ["matriculaal", "datanascimentoal"],
                ["primeironomeal", "ultimonomeal"],
                ["senhaal", "idturma"]
            ]
        )
        self.forms.build(self.send)
