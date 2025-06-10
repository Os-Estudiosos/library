from gui.screens import Screen
import customtkinter as ctk
import pandas as pd
from config.colors import Colors
from gui.manager.routemanager import RouteManager
import tkinter as tk

from gui.screens.components.table import Table
from gui.screens.components.forms import Form
from gui.screens.components.empty import EmptyFrame

from gui.manager.tablesmanager import TablesManager


class Classes(Screen):
    def __init__(self, app):
        self.app = app

        self.items_per_page=10

    def build(self, **kwargs):
        if "page" in kwargs.keys():
            page = kwargs["page"]
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
            text="Turmas",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Lista com todas as turmas registradas na livraria",
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
            command=lambda: RouteManager.go_to("create_class"),
            width=100,
            text_color="#fff",
            corner_radius=10
        )
        add_button.grid(column=0, row=0, ipady=5, padx=(0, 10), sticky="e")

        filter_button = ctk.CTkButton(
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
        filter_button.grid(column=1, row=0, ipady=5)

        buttons_frame.grid(column=1, row=0, rowspan=2, sticky="nsew")

        title_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        pagination = TablesManager.turmaTable.read(qtd=self.items_per_page, pagina=page)

        if pagination:
            table = Table(self.app, "edit_classes", TablesManager.turmaTable, "idturma", "see_class")
            table.build(pagination)
        else:
            empty_frame = EmptyFrame(self.app)
            empty_frame.build()


class EditClass(Screen):
    def __init__(self, app):
        self.app = app

        self.current_id = None
    
    def build(self, **kwargs):
        self.current_id = kwargs["entry"]["idturma"]
        library_class = TablesManager.turmaTable.read_one(
            idturma=self.current_id,
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
            text="Editar Turma",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text=f"Você está editando a turma de {library_class["nometurma"]}",
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
                "nometurma": {
                    "label": "Nome da Turma:",
                    "intype": "entry",
                    "placeholder": "Ex: Redes de Computadores"
                },
            },
            entry_dict={
                "nometurma": tk.StringVar(),
            },
            layout=[
                ["nometurma"],
            ]
        )
        self.forms.build(self.send, library_class)
    
    def send(self):
        values = self.forms.get_values()
        TablesManager.turmaTable.update({
            "idturma": self.current_id,
        },values)
        RouteManager.go_back()


class CreateClass(Screen):
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
            text="Criar Turma",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Você vai criar um registro de uma turma, insira as informações e clique em INSERIR",
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
                "nometurma": {
                    "label": "Nome da Turma:",
                    "intype": "entry",
                    "placeholder": "Ex: Redes de Computadores"
                },
            },
            entry_dict={
                "nometurma": tk.StringVar(),
            },
            layout=[
                ["nometurma"],
            ]
        )
        self.forms.build(self.send)
    
    def send(self):
        values = self.forms.get_values()
        qtd = TablesManager.turmaTable.read(qtd=1,pagina=1)["total_registros"]
        TablesManager.turmaTable.create({
            "idturma": qtd+1,
        },values)
        RouteManager.go_back()


class SeeClass(Screen):
    def __init__(self, app):
        self.app = app
        self.items_per_page = 10

    def build(self, **kwargs):
        actual_class = kwargs["entry"]

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
            text=f"{actual_class.nometurma}",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text=f"Alunos presentes na turma {actual_class.nometurma}",
            font=("Arial", 15, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        description.grid(column=0, row=1, sticky="w")

        cancel_button = ctk.CTkButton(
            title_frame,
            command=lambda: RouteManager.go_to("classes"),
            fg_color="#ffffff",
            hover_color=Colors.GRAY.c_100,
            text_color=Colors.GRAY.c_800,
            border_color=Colors.GRAY.c_300,
            border_width=1,
            text="Voltar",
            font=("Arial", 13, "bold"),
            width=100,
            corner_radius=10
        )
        cancel_button.grid(column=1, row=0, ipady=5, rowspan=2, sticky="e")

        title_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        if "page" in kwargs.keys():
            page = kwargs["page"]
        else:
            page = 1
        
        pagination = TablesManager.alunoTable.read(filter={
            "idturma": int(actual_class.idturma)
        }, qtd=self.items_per_page, pagina=page)

        if pagination:
            table = Table(self.app, "edit_students", TablesManager.alunoTable, "matriculaal")
            table.build(pagination)
        else:
            empty_frame = EmptyFrame(self.app)
            empty_frame.build()
