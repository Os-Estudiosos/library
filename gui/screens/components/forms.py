import customtkinter as ctk

from config.colors import Colors

from gui.screens.components.input import Input, SearchSelect


class Form:
    def __init__(self, master, form_dict, entry_dict, layout):
        self.master = master
        self.forms_frame = ctk.CTkFrame(
            self.master,
            fg_color="#fff"
        )

        self.form_dict = form_dict

        self.student_dict = entry_dict

        self.layout = layout

        self.inputs=[]

    def build(self, send_function, entry=None):
        for i, line in enumerate(self.layout):
            for j, key in enumerate(line):
                self.forms_frame.rowconfigure(i, weight=1)
                self.forms_frame.columnconfigure(j, weight=1)
                if key is not None:
                    wrapper = ctk.CTkFrame(
                        self.forms_frame,
                        fg_color="transparent"
                    )
                    wrapper.rowconfigure(0, weight=1)
                    wrapper.rowconfigure(1, weight=1)

                    label = ctk.CTkLabel(
                        wrapper,
                        text=self.form_dict[key]["label"],
                        text_color=Colors.GRAY.c_600
                    )
                    label.grid(row=0, column=0, sticky="w")

                    match self.form_dict[key]["intype"]:
                        case "entry":
                            input = Input(
                                master=wrapper,
                                name=key,
                                placeholder_text=self.form_dict[key]["placeholder"],
                                border_width=1,
                                width=450,
                            )
                            input.grid(row=1, column=0, sticky="ew")
                            if entry is not None:
                                input.insert(0, entry[key])
                        case "search":
                            input = SearchSelect(
                                master=wrapper,
                                name=key,
                                table=self.form_dict[key]["table"],
                                exihibition_column=self.form_dict[key]["exihibition_column"],
                                value_column=self.form_dict[key]["value_column"]
                            )
                            input.grid(row=1, column=0, sticky="ew")
                            if entry is not None:
                                input.insert(entry[key])

                    self.inputs.append(input)
                    wrapper.grid(row=i, column=j, padx=10, pady=(10, 0), sticky="ew")
        
        self.forms_frame.grid(row=1, column=0, sticky="nswe", padx=10)

        confirm_button = ctk.CTkButton(
            self.forms_frame,
            text="Confirmar",
            font=("Arial", 14, "bold"),
            fg_color=Colors.INDIGO.c_600,
            hover_color=Colors.INDIGO.c_700,
            command=send_function,
            text_color="#fff",
            width=100,
            corner_radius=10
        )
        confirm_button.grid(row=i+1, column=0, ipady=5, sticky="w", padx=10, pady=(10, 10))
    
    def get_values(self):
        values = {}
        for input in self.inputs:
            values[input.name] = input.get()
        return values
