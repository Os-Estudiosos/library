import customtkinter as ctk

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
