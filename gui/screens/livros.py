from gui.screens import Screen
import customtkinter as ctk
from config.colors import Colors
import pandas as pd
import numpy as np

from gui.manager.routemanager import RouteManager

from gui.screens.components.table import Table
from gui.screens.components.forms import Form

from gui.manager.tablesmanager import TablesManager

import tkinter as tk


class Books(Screen):
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
            text="Livros",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Lista com todos os livros registrados na livraria",
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
            text_color="#fff",
            fg_color=Colors.INDIGO.c_600,
            hover_color=Colors.INDIGO.c_700,
            command=lambda: RouteManager.go_to("create_book"),
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

        if "page" in kwargs.keys():
            page = kwargs["page"]
        else:
            page = 1

        pagination = TablesManager.livroTable.read(qtd=self.items_per_page, pagina=page)

        table = Table(self.app, "edit_books", TablesManager.livroTable, "isbnliv")
        table.build(pagination)


class EditBook(Screen):
    def __init__(self, app):
        self.app = app
        self.current_isbnliv = None
    
    def build(self, *args, **kwargs):
        self.current_isbnliv = kwargs["entry"]["isbnliv"]
        book = TablesManager.livroTable.read_one(
            isbnliv=self.current_isbnliv,
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
            text=f"Editar {book.nomeliv}",
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
                "isbnliv": {
                    "label": "ISBN:",
                    "intype": "entry",
                    "placeholder": "Ex: 0392839"
                },
                "nomeliv": {
                    "label": "Nome do Livro:",
                    "intype": "entry",
                    "placeholder": "Ex: José"
                },
                "editoraliv": {
                    "label": "Editora:",
                    "intype": "entry",
                    "placeholder": "Ex: Alberto"
                },
                "edicaoliv": {
                    "label": "Edição:",
                    "intype": "entry",
                    "placeholder": "Ex: 20-13-2005"
                },
                "anolancamentoliv": {
                    "label": "Ano de Lançamento:",
                    "intype": "entry",
                    "placeholder": "Ex: axzoue!Lso$p028"
                },
                "idgru": {
                    "label": "Grupo:",
                    "intype": "search",
                    "table": TablesManager.grupoTable,
                    "exihibition_column": "nomegru",
                    "value_column": "idgru"
                }
            },
            entry_dict={
                "isbnliv": tk.StringVar(),
                "nomeliv": tk.StringVar(),
                "editoraliv": tk.StringVar(),
                "edicaoliv": tk.StringVar(),
                "anolancamentoliv": tk.StringVar(),
                "idgru": tk.StringVar()
            },
            layout=[
                ["nomeliv", "isbnliv"],
                ["editoraliv", "edicaoliv"],
                ["anolancamentoliv", "idgru"]
            ]
        )
        self.forms.build(self.send, book)
    
    def send(self):
        values = self.forms.get_values()
        for k, v in values.items():
            if isinstance(v, np.int64):
                values[k] = int(v)
        del values["isbnliv"]
        TablesManager.livroTable.update({
            "isbnliv": self.current_isbnliv,
        },values)
        RouteManager.go_back() 


class CreateBook(Screen):
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
            text="Criar Livro",
            font=("Arial", 20, "bold"),
            text_color=Colors.SLATE.c_900,
            justify="left"
        )
        title.grid(column=0, row=0, sticky="w")

        description = ctk.CTkLabel(
            title_frame,
            text="Você vai criar um registro de um livro, insira as informações e clique em INSERIR",
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
                "isbnliv": {
                    "label": "ISBN:",
                    "intype": "entry",
                    "placeholder": "Ex: 0392839"
                },
                "nomeliv": {
                    "label": "Nome do Livro:",
                    "intype": "entry",
                    "placeholder": "Ex: José"
                },
                "editoraliv": {
                    "label": "Editora:",
                    "intype": "entry",
                    "placeholder": "Ex: Alberto"
                },
                "edicaoliv": {
                    "label": "Edição:",
                    "intype": "entry",
                    "placeholder": "Ex: 20-13-2005"
                },
                "anolancamentoliv": {
                    "label": "Ano de Lançamento:",
                    "intype": "entry",
                    "placeholder": "Ex: axzoue!Lso$p028"
                },
                "idgru": {
                    "label": "Grupo:",
                    "intype": "search",
                    "table": TablesManager.grupoTable,
                    "exihibition_column": "nomegru",
                    "value_column": "idgru"
                }
            },
            entry_dict={
                "isbnliv": tk.StringVar(),
                "nomeliv": tk.StringVar(),
                "editoraliv": tk.StringVar(),
                "edicaoliv": tk.StringVar(),
                "anolancamentoliv": tk.StringVar(),
                "idgru": tk.StringVar()
            },
            layout=[
                ["nomeliv", "isbnliv"],
                ["editoraliv", "edicaoliv"],
                ["anolancamentoliv", "idgru"]
            ]
        )
        self.forms.build(self.send)
    
    def send(self):
        values = self.forms.get_values()
        for k, v in values.items():
            if isinstance(v, np.int64):
                values[k] = int(v)
        isbn = values["isbnliv"]
        del values["isbnliv"]
        TablesManager.livroTable.create({
            "isbnliv": isbn,
        },values)
        RouteManager.go_back()
