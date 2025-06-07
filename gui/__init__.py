import customtkinter as ctk
import platform
from typing import Any
import os

from gui.screens.alunos import Students
from gui.screens.livros import Books
from gui.screens.atendentes import Secretaries
from gui.screens.categorias import Categories
from gui.screens.emprestimos import Loans
from gui.screens.grupos import Groups
from gui.screens.reservas import Reserves
from gui.screens.suspensoes import Suspensions
from gui.screens.turma import Classes

from gui.screens.layout import Layout


class Application(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Alex Jerônimo Falqueto")  # Colocando o título da aplicação

        self.default = "students"  # Definindo a tela padrão
        self.active = self.default

        self.layout = Layout(self)  # Iniciando o layout

        self.screens = {  # Definindo minhas telas
            "students": Students(self.layout.frame),
            "books": Books(self.layout.frame),
            "secretaries": Secretaries(self.layout.frame),
            "categories": Categories(self.layout.frame),
            "loans": Loans(self.layout.frame),
            "groups": Groups(self.layout.frame),
            "reserves": Reserves(self.layout.frame),
            "suspensions": Suspensions(self.layout.frame),
            "classes": Classes(self.layout.frame),
        }

        # Configurações para que a tela fique corretamente na grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
    
    def delete_previous_screen(self):
        """Destroy the elements of the previous page
        """
        self.layout.restart()  # Reinicio o layout (Frame dentro)
    
    def initialize(self, arguments=None):
        self.layout.build()  # Construindo o layout logo na inicialização
        self.screens[self.default].build(arguments)

        if platform.system() == "Windows":
            self.state("zoomed")
        else:
            self.attributes("-zoomed", True)
    
    def go_to(self, screen: str, arguments: Any = None):
        """Go to a specific page

        Args:
            screen (str): Name of the page
            arguments (Any): Arguments to pass to the page
        """
        self.delete_previous_screen()
        self.active = screen
        self.layout.build()
        self.screens[screen].build(arguments)
