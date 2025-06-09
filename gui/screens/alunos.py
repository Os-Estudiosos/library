from gui.screens import Screen
import customtkinter as ctk
import pandas as pd

from gui.screens.components.table import Table


class Students(Screen):
    def __init__(self, app):
        self.app = app

    def build(self, *args, **kwargs):
        label = ctk.CTkLabel(
            self.app,
            text="Alunos"
        )
        label.grid(column=0, row=0)
        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        students = pd.read_csv("gui/screens/students.csv")

        table = Table(self.app, "edit_aluno")
        table.build(students)
