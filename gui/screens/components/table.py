import customtkinter as ctk
import pandas as pd
from config.colors import Colors

from gui.screens.components.actions import EditButton, TrashButton, SeeButton
from gui.screens.components.pagination import Pagination


class Table:
    def __init__(self, master, go_on_edit, table, primary_key, go_on_see=None):
        self.app = master
        self.go_on_edit = go_on_edit
        self.go_on_see = go_on_see
        self.primary_key = primary_key
        self.table = table
    
    def build(self, pagination):
        if pagination:
            table = pagination["registros"]

            upper_frame = ctk.CTkFrame(self.app, fg_color=Colors.GRAY.c_50)  # Criando o frame da tabela inteira
            upper_frame.rowconfigure(0, weight=1)
            upper_frame.columnconfigure(0, weight=1)

            frame = ctk.CTkFrame(upper_frame, fg_color=Colors.GRAY.c_50)  # Criando o frame interno

            for j, column in enumerate(table.columns): # Adicionando o Cabeçalho
                frame.columnconfigure(j, weight=1)  # Configurando para que a coluna expanda
                column_cell = ctk.CTkFrame(
                    frame,
                    fg_color=Colors.GRAY.c_50,
                    corner_radius=0
                )
                column_cell.grid(row=0, column=j, sticky='ew')  # Expandindo para ficar bonito
                
                column_label = ctk.CTkLabel(  # Adicionando o texto;
                    column_cell,
                    text=column,
                    font=("Arial", 14, "bold"),
                    text_color=Colors.SLATE.c_800,
                )
                column_label.grid(row=0, column=0, sticky='w', padx=(10, 0), pady=(0, 5))  # Expandindo para ficar bonito

            frame.columnconfigure(j+1, weight=1)  # Coluna extra padrão

            column_cell = ctk.CTkFrame(
                frame,
                fg_color="#F9FAFB",
                corner_radius=0
            )
            column_cell.grid(row=0, column=j+1, sticky='ew')  # Expandindo para ficar bonito
            column_cell.rowconfigure(0, weight=1)  # Coluna extra padrão
            column_cell.columnconfigure(0, weight=1)  # Coluna extra padrão

            column_label = ctk.CTkLabel(  # Texto
                column_cell,
                text="Opções",
                font=("Arial", 14, "bold"),
                justify="center",
                text_color=Colors.SLATE.c_800,
            )
            column_label.grid(row=0, column=0, sticky='ew', padx=(10, 0), pady=(0, 5))  # Alinhando bonitinho


            # Linha de divisão entre cabeçalho e linhas
            line = ctk.CTkFrame(
                frame,
                fg_color=Colors.GRAY.c_400,
                height=2
            )
            line.grid(row=1, column=0, columnspan=j+2, sticky="ew")


            for datapoint in table.iterrows():  # Adicionando os valores da tabela
                i = datapoint[0]+1
                frame.rowconfigure(i, weight=1)
                for j, value in enumerate(datapoint[1]):  # Indo em cada coluna
                    cell = ctk.CTkFrame(
                        frame,
                        fg_color=Colors.GRAY.c_50 if i%2==0 else Colors.GRAY.c_100,
                        corner_radius=0
                    )
                    cell.grid(row=i+1, column=j, sticky='nsew')
                    cell.rowconfigure(0, weight=1)
                    cell.columnconfigure(0, weight=1)

                    label = ctk.CTkLabel(
                        cell,
                        text=value,
                        height=14,
                        text_color=Colors.SLATE.c_500
                    )
                    label.grid(row=0, column=0, sticky='nsw', padx=(10, 0))
                
                actions_frame = ctk.CTkFrame(  # Adicionando o frame dos botões
                    frame,
                    fg_color=Colors.GRAY.c_50 if i%2==0 else Colors.GRAY.c_100,
                    corner_radius=0,
                    height=14
                )
                actions_frame.grid(row=i+1, column=j+1, sticky="ew")  # Posicionando ele na grid

                if self.go_on_see is not None:
                    actions_frame.columnconfigure(0, weight=1)
                    actions_frame.columnconfigure(2, weight=1)
                    actions_frame.rowconfigure(0, weight=1)

                    see_button = SeeButton(self.go_on_see, datapoint[1], actions_frame)
                    see_button.grid(row=0, column=0, pady=5, padx=5, sticky="e")
                    edit_button = EditButton(self.go_on_edit, datapoint[1], actions_frame)
                    edit_button.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
                    trash_icon = TrashButton((
                        self.table,
                        self.primary_key,
                        datapoint[1][self.primary_key]
                    ), actions_frame)
                    trash_icon.grid(row=0, column=2, pady=5, padx=5, sticky="w")
                else:
                    actions_frame.columnconfigure(0, weight=1)
                    actions_frame.columnconfigure(1, weight=1)

                    edit_button = EditButton(self.go_on_edit, datapoint[1], actions_frame)
                    edit_button.grid(row=0, column=0, pady=5, padx=5, sticky="e")
                    trash_icon = TrashButton((
                        self.table,
                        self.primary_key,
                        datapoint[1][self.primary_key]
                    ), actions_frame)
                    trash_icon.grid(row=0, column=1, pady=5, padx=5, sticky="w")

            line = ctk.CTkFrame(
                frame,
                fg_color=Colors.GRAY.c_400,
                height=2
            )
            line.grid(row=datapoint[0]+3, column=0, columnspan=j+2, sticky="ew")

            pagination_frame = ctk.CTkFrame(
                frame,
                fg_color="transparent",
            )
            pagination_frame.grid(row=datapoint[0]+4, column=0, columnspan=j+2, sticky="nsew", pady=(5,0))

            pagination_frame.columnconfigure(0, weight=1)
            pagination_frame.columnconfigure(1, weight=1)

            pagination_widget = Pagination(
                pagination_frame,
                pagination
            )
            pagination_widget.build()

            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            upper_frame.grid(row=1, column=0, sticky="ew", padx=20)
