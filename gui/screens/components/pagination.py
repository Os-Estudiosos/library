import customtkinter as ctk
from config.colors import Colors
from PIL import Image
import os

from gui.manager.routemanager import RouteManager


class Pagination:
    def __init__(self, master, pagination):
        self.pagination = pagination
        self.master = master
    
    def build(self):
        pagination_text = ctk.CTkLabel(
            self.master,
            text_color=Colors.GRAY.c_600,
            text=f"Mostrando {self.pagination["registros_por_pagina"]} registros de {self.pagination["total_registros"]}"
        )
        pagination_text.grid(row=0, column=0, sticky="w", padx=10)

        buttons_frame = ctk.CTkFrame(
            self.master,
            fg_color=Colors.GRAY.c_200,
            corner_radius=5
        )
        buttons_frame.grid(row=0, column=1, sticky="nse", padx=10)

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.rowconfigure(0, weight=1)

        internal_buttons_frame = ctk.CTkFrame(
            buttons_frame,
            fg_color="#fff",
            corner_radius=0
        )
        internal_buttons_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        arrow_right_image = Image.open(os.path.join(os.getcwd(), "gui", "images", "arrow.png"))
        arrow_right_image_ctk = ctk.CTkImage(
            light_image=arrow_right_image,
            size=(16, 16)
        )

        arrow_left_image = arrow_right_image.rotate(180)
        arrow_left_image_ctk = ctk.CTkImage(
            light_image=arrow_left_image,
            size=(16, 16)
        )

        arrow_left_btn = ctk.CTkButton(
            internal_buttons_frame,
            fg_color="#fff",
            hover_color=Colors.GRAY.c_200,
            text_color=Colors.GRAY.c_500,
            command=lambda: RouteManager.go_to(
                RouteManager.active,
                page=self.pagination["pagina_atual"]-1
            ),
            image=arrow_left_image_ctk,
            state="disabled" if self.pagination["pagina_atual"]==1 else "normal",
            width=30,
            text="",
            corner_radius=0
        )
        arrow_left_btn.grid(row=0, column=0, sticky="ns")

        cont = 0
        for i in range(self.pagination["total_paginas"]):
            if self.pagination["total_paginas"] > 6 and 2 <= i <= self.pagination["total_paginas"]-3:
                cont += 1

                if cont == 1:
                    continue_label = ctk.CTkLabel(
                        internal_buttons_frame,
                        fg_color="#fff",
                        text_color=Colors.GRAY.c_500,
                        text=f"...",
                        width=50,
                        corner_radius=0
                    )
                    continue_label.grid(row=0, column=i+1)
                
                if i+1 == self.pagination["pagina_atual"]:
                    i_btn = ctk.CTkButton(
                        internal_buttons_frame,
                        fg_color=Colors.INDIGO.c_600,
                        text_color_disabled="#fff",
                        hover_color=Colors.INDIGO.c_600,
                        text_color="#fff",
                        text=f"{i+1}",
                        width=30,
                        state="disabled",
                        corner_radius=0
                    )
                    i_btn.grid(row=0, column=i+1, padx=(2, 0))

                    continue_label = ctk.CTkLabel(
                        internal_buttons_frame,
                        fg_color="#fff",
                        text_color=Colors.GRAY.c_500,
                        text=f"...",
                        width=50,
                        corner_radius=0
                    )
                    continue_label.grid(row=0, column=i+2)

                continue

            def btn_callback(page=i):
                RouteManager.go_to(
                    RouteManager.active,
                    **{
                        k: v for k, v in RouteManager.history[-1]["arguments"].items() if k != "page"
                    },
                    page=page+1
                )

            i_btn = ctk.CTkButton(
                internal_buttons_frame,
                fg_color=Colors.INDIGO.c_600 if i+1 == self.pagination["pagina_atual"] else "#fff",
                text_color_disabled="#fff",
                hover_color=Colors.INDIGO.c_600 if i+1 == self.pagination["pagina_atual"] else Colors.GRAY.c_200,
                text_color="#fff" if i+1 == self.pagination["pagina_atual"] else Colors.GRAY.c_500,
                command=btn_callback,
                text=f"{i+1}",
                width=30,
                state="disabled" if i+1 == self.pagination["pagina_atual"] else "normal",
                corner_radius=0,
            )
            i_btn.grid(row=0, column=i+1, padx=(2, 0))

        arrow_right_btn = ctk.CTkButton(
            internal_buttons_frame,
            fg_color="#fff",
            hover_color=Colors.GRAY.c_200,
            text_color=Colors.GRAY.c_500,
            command=lambda: RouteManager.go_to(
                RouteManager.active,
                page=self.pagination["pagina_atual"]+1
            ),
            image=arrow_right_image_ctk,
            width=30,
            state="disabled" if self.pagination["pagina_atual"]==self.pagination["total_paginas"] else "normal",
            text="",
            corner_radius=0
        )
        arrow_right_btn.grid(row=0, column=i+2, sticky="ns")
