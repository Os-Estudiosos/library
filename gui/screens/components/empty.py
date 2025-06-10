import customtkinter as ctk

from config.colors import Colors


class EmptyFrame:
    def __init__(self, master):
        self.master = master
        self.frame=ctk.CTkFrame(
            self.master,
            fg_color="transparent"
        )
    
    def build(self):
        self.frame.grid(row=1, column=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        intern_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        intern_frame.grid(row=0, column=0, sticky="nsew")

        intern_frame.columnconfigure(0, weight=1)
        intern_frame.rowconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            intern_frame,
            text="Oh Ou...",
            text_color=Colors.GRAY.c_700,
            font=("Arial", 25, "bold")
        )
        titulo.grid(row=0, column=0, sticky="ns")

        description = ctk.CTkLabel(
            intern_frame,
            text="Não encontramos nenhum registro no banco",
            text_color=Colors.GRAY.c_500,
            font=("Arial", 18, "bold")
        )
        description.grid(row=1, column=0, sticky="ns")
