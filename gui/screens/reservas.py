from gui.screens import Screen
import customtkinter as ctk


class Reserves(Screen):
    def __init__(self, app):
        self.app = app

    def build(self, *args, **kwargs):
        label = ctk.CTkLabel(
            self.app,
            text="Reservas"
        )
        label.grid(column=0, row=0)
