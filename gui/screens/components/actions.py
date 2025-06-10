import customtkinter as ctk
from PIL import Image
import os
from config.colors import Colors
from gui.manager.routemanager import RouteManager
from utils.word import wrap_text


class SeeButton:
    def __init__(
        self,
        route,
        route_arguments,
        master
    ):
        self.route = route
        self.master = master

        def on_click():
            RouteManager.go_to(route, route_arguments)

        self.image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "gui", "images", "eye-icon.png")),
            size=(16, 16)
        )

        self.__button = ctk.CTkButton(
            self.master,
            command=on_click,
            fg_color=Colors.EMERALD.c_600,
            hover_color=Colors.EMERALD.c_700,
            image=self.image,
            text="",
            width=25,
            height=25
        )
    
    def grid(self, **kwargs):
        self.__button.grid(**kwargs)

class EditButton:
    def __init__(
        self,
        route,
        route_arguments,
        master
    ):
        self.route = route
        self.master = master

        def on_click():
            RouteManager.go_to(route, route_arguments)

        self.image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "gui", "images", "edit-icon.png")),
            size=(16, 16)
        )

        self.__button = ctk.CTkButton(
            self.master,
            command=on_click,
            image=self.image,
            text="",
            width=25,
            height=25
        )
    
    def grid(self, **kwargs):
        self.__button.grid(**kwargs)


class TrashButton:
    def __init__(
        self,
        arguments,
        master
    ):
        self.master = master

        self._image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "gui", "images", "trash-icon.png")),
            size=(16, 16)
        )

        self.__button = ctk.CTkButton(
            self.master,
            image=self._image,
            command=lambda: self.delete_entry(arguments[0], arguments[1], arguments[2]),
            text="",
            width=25,
            height=25,
            fg_color=Colors.ROSE.c_600,
            hover_color=Colors.ROSE.c_700
        )
    
    def grid(self, **kwargs):
        self.__button.grid(**kwargs)
    
    def delete_entry(self, table, primary_key, primary_key_value):
        """_summary_

        Args:
            arguments (_type_): _description_
        """
        # Cria a sobreposição (janela sem bordas)
        root = RouteManager.app
        overlay = ctk.CTkFrame(root, fg_color=Colors.VIOLET.c_200)

        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        overlay.columnconfigure(0, weight=1)
        overlay.rowconfigure(0, weight=1)

        box = ctk.CTkFrame(  # Caixa do MODAL
            overlay,
            corner_radius=10,
            fg_color="#ffffff",
        )
        box.grid(row=0, column=0)

        box.rowconfigure(0, weight=1)
        box.rowconfigure(1, weight=1)
        box.rowconfigure(2, weight=1)

        # Colocando os elementos dentro do box
        icon = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "gui", "images", "warning-icon.png")),
            size=(36, 36)
        )
        warning_icon = ctk.CTkLabel(
            box,
            image=icon,
            text="",
        )
        warning_icon.grid(row=0, column=0, padx=(10, 5), pady=(10,0), sticky="ewn")

        label_title = ctk.CTkLabel(
            box,
            text="Deletando Registro",
            font=("Arial", 23, "bold"),
            text_color=Colors.SLATE.c_900
        )
        label_title.grid(row=0,column=1, sticky="w", padx=10, pady=(10,0))

        label_description = ctk.CTkLabel(
            box,
            text=wrap_text("Tem certeza de que deseja deletar esse registro? Essa ação é irreversível, tenha certeza ABSOLUTA do que está fazendo e das consequências", 55),
            text_color=Colors.SLATE.c_500,
            justify="left",
            font=("Arial", 15)
        )
        label_description.grid(row=1,column=1, sticky="nw", padx=10, pady=(0, 10))

        buttons_container = ctk.CTkFrame(
            box,
            fg_color="transparent"
        )
        buttons_container.grid(column=1, row=2, sticky="w", pady=(0, 15))

        def delete_btn_callback():
            if isinstance(primary_key, tuple):
                keys = {}
                for i in range(len(primary_key)):
                    keys[primary_key[i]] = primary_key_value[i]
                table.delete(keys)
            else:
                table.delete({
                    f"{primary_key}": primary_key_value
                })
            overlay.destroy()
            RouteManager.go_to(RouteManager.active)

        confirm_button = ctk.CTkButton(
            buttons_container,
            command=delete_btn_callback,
            fg_color=Colors.RED.c_500,
            hover_color=Colors.RED.c_700,
            text_color="#ffffff",
            text="Deletar",
            font=("Arial", 13, "bold"),
            width=100
        )
        confirm_button.grid(column=0, row=0, padx=(10, 5))

        cancel_button = ctk.CTkButton(
            buttons_container,
            command=overlay.destroy,
            fg_color="#ffffff",
            hover_color=Colors.GRAY.c_100,
            text_color=Colors.GRAY.c_800,
            border_color=Colors.GRAY.c_300,
            border_width=1,
            text="Cancelar",
            font=("Arial", 13, "bold"),
            width=100
        )
        cancel_button.grid(column=1, row=0, padx=5)
