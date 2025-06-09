import customtkinter as ctk
import pandas as pd
from config.colors import Colors
from gui.screens.components.actions import EditButton, TrashButton


class Table:
    def __init__(self, master, go_on_edit):
        self.app = master
        self.go_on_edit = go_on_edit
    
    def build(self, table: pd.DataFrame):
        frame = ctk.CTkFrame(self.app, fg_color=Colors.GRAY.c_50)  # Criando o frame da tabela inteira

        for j, column in enumerate(table.columns): # Adicionando o Cabeçalho
            frame.columnconfigure(j, weight=1)  # Configurando para que a coluna expanda
            column_label = ctk.CTkLabel(  # Adicionando o texto;
                frame,
                text=column,
                font=("Arial", 14, "bold")
            )
            column_label.grid(row=0, column=j, sticky='ew')  # Expandindo para ficar bonito
        frame.columnconfigure(j+1, weight=1)  # Coluna extra padrão
        column_label = ctk.CTkLabel(  # Texto
            frame,
            text="Opções",
            font=("Arial", 14, "bold")
        )
        column_label.grid(row=0, column=3, sticky='ew')  # Alinhando bonitinho
        
        table = table.to_numpy()  # Transformando a tabela em numpy para mexer melhor

        for i, datapoint in enumerate(table):  # Adicionando os valores da tabela
            frame.rowconfigure(i, weight=1)
            for j, value in enumerate(datapoint):  # Indo em cada coluna
                color = Colors.INDIGO.c_100
                if i % 2 == 1:
                    color = Colors.GRAY.c_50

                label = ctk.CTkLabel(
                    frame,
                    text=value,
                    padx=5,
                    pady=5,
                    fg_color=color,
                    height=14
                )
                label.grid(row=i+1, column=j, sticky='nsew')
            
            actions_frame = ctk.CTkFrame(  # Adicionando o frame dos botões
                frame,
                fg_color=color,
                corner_radius=0,
                height=14
            )
            actions_frame.grid(row=i+1, column=j+1, sticky="ew")  # Posicionando ele na grid

            actions_frame.columnconfigure(0, weight=1)
            actions_frame.columnconfigure(1, weight=1)
            actions_frame.rowconfigure(0, weight=1)

            edit_button = EditButton(self.go_on_edit, "meh", "meh meh", actions_frame)
            edit_button.grid(row=0, column=0, pady=5, padx=5, sticky="e")
            trash_icon = TrashButton(self.go_on_edit, "meh", "meh meh", actions_frame)
            trash_icon.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        frame.grid(row=1, column=0, sticky="ew")
