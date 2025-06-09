import customtkinter as ctk
import platform
from typing import Any
import os
from gui.manager.routemanager import RouteManager

from gui.screens.layout import Layout


class Application(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Alex Jerônimo Falqueto")  # Colocando o título da aplicação

        self.layout = Layout(self)  # Iniciando o layout

        # Configurações para que a tela fique corretamente na grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
    
    def delete_previous_screen(self):
        """Destroy the elements of the previous page
        """
        self.layout.restart()  # Reinicio o layout (Frame dentro)
    
    def initialize(self, arguments=None):
        self.layout.build()  # Construindo o layout logo na inicialização
        RouteManager.go_to(RouteManager.default)

        if platform.system() == "Windows":
            self.state("zoomed")
        else:
            self.attributes("-zoomed", True)
