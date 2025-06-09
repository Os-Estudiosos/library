import customtkinter as ctk
from PIL import Image
import os
from config.colors import Colors


class EditButton:
    def __init__(
        self,
        route,
        root_application,
        route_arguments,
        master
    ):
        self.root_application = root_application
        self.route = route
        self.master = master

        def on_click():
            self.root_application.go_to(route, route_arguments)

        self._image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "gui", "images", "edit-icon.png")),
            size=(20, 20)
        )

        self.__button = ctk.CTkButton(
            self.master,
            command=on_click,
            image=self._image,
            text="",
            width=20,
            height=20
        )
    
    def grid(self, **kwargs):
        self.__button.grid(**kwargs)


class TrashButton:
    def __init__(
        self,
        route,
        root_application,
        route_arguments,
        master
    ):
        self.root_application = root_application
        self.route = route
        self.master = master

        def on_click():
            self.root_application.go_to(route, route_arguments)

        self._image = ctk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "gui", "images", "trash-icon.png")),
            size=(20, 20)
        )

        self.__button = ctk.CTkButton(
            self.master,
            command=on_click,
            image=self._image,
            text="",
            width=20,
            height=20,
            fg_color=Colors.ROSE.c_600,
            hover_color=Colors.ROSE.c_700
        )
    
    def grid(self, **kwargs):
        self.__button.grid(**kwargs)

