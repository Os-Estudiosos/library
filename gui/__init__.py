import customtkinter as ctk
import platform
from typing import Any

from gui.screens.login import Login
from gui.screens.home import Home
from gui.screens.layout import Layout


class Application(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.title("Alex Jerônimo Falqueto")

        self.screens = {
            "login": Login(self),
            "home": Home(self)
        }
        self.layout = Layout(self)
        self.default = "home"
        self.history = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
    
    def delete_previous_screen(self):
        """Destroy the elements of the previous page
        """
        for i in self.winfo_children():
            i.destroy()
    
    def initialize(self, arguments=None):
        self.layout.build()
        self.screens[self.default].build(arguments)
        self.history.append({
            "page": self.default,
            "arguments": arguments
        })

        if platform.system() == "Windows":
            self.state("zoomed")
        else:
            self.attributes("-zoomed", True)
    
    def go_back(self):
        self.delete_previous_screen()
        self.layout.build()
        self.screens[self.history[-2]["page"]].build(self.history[-2]["arguments"])
        self.history.pop()
    
    def go_to(self, screen: str, arguments: Any = None):
        """Go to a specific page

        Args:
            screen (str): Name of the page
            arguments (Any): Arguments to pass to the page
        """
        self.delete_previous_screen()
        self.history.append({
            "page": screen,
            "arguments": arguments
        })
        self.layout.build()
        self.screens[screen].build(arguments)
