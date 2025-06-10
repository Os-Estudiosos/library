import customtkinter as ctk
import pandas as pd
from config.colors import Colors


class Input(ctk.CTkEntry):
    def __init__(self, master, name, **kwargs):
        super().__init__(master, **kwargs)
        self.name = name
        self._entry.bind("<Shift-Left>", self.select_left)
        self._entry.bind("<Shift-Right>", self.select_right)
        self._entry.bind("<Home>", lambda e: self._entry.icursor(0))
        self._entry.bind("<End>", lambda e: self._entry.icursor("end"))

        # Outros atalhos úteis:
        self._entry.bind("<Control-a>", self.select_all)
        self._entry.bind("<Control-A>", self.select_all)

    def select_left(self, event):
        pos = self._entry.index("insert")
        if pos > 0:
            self._entry.selection_range(pos - 1, pos)
            self._entry.icursor(pos - 1)
        return "break"

    def select_right(self, event):
        pos = self._entry.index("insert")
        if pos < len(self.get()):
            self._entry.selection_range(pos, pos + 1)
            self._entry.icursor(pos + 1)
        return "break"

    def select_all(self, event):
        self._entry.selection_range(0, "end")
        self._entry.icursor("end")
        return "break"


class SearchSelect:
    def __init__(self, master, name, table, exihibition_column, value_column, **kwargs):
        self.master = master
        self.table = table
        self.name = name
        self.exihibition_column = exihibition_column
        self.value_column = value_column
        self.boxoption = None
        self.options = None
        self.dataframe = pd.read_csv(f"gui/screens/csv/{self.table}.csv")

        self.restart(**kwargs)
    
    def restart(self, **kwargs):
        self.options = self.dataframe[self.exihibition_column]
        self.boxoption = ctk.CTkOptionMenu(
            master=self.master,
            values=self.options,
            fg_color=Colors.GRAY.c_100,
            button_color=Colors.GRAY.c_300,
            button_hover_color=Colors.GRAY.c_400,
            text_color=Colors.GRAY.c_700
        )
    
    def insert(self, *args):
        index = args[0]
        value = self.dataframe[self.dataframe[self.value_column]==index][self.exihibition_column].iloc[0]
        self.boxoption.set(value)
    
    def grid(self, **kwargs):
        self.boxoption.grid(**kwargs)
