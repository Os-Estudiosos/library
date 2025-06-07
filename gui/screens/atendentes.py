from gui.screens import Screen
import customtkinter as ctk


class Secretaries(Screen):
    def __init__(self, app):
        self.app = app

    def build(self, *args, **kwargs):
        label = ctk.CTkLabel(
            self.app,
            text="Atendentes"
        )
        label.grid(column=0, row=0)
