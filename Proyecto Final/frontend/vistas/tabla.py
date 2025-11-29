from tkinter import ttk

class Tabla(ttk.Treeview):
    def __init__(self, master, columns, **kwargs):
        super().__init__(master, columns=columns, show='headings', **kwargs)
        for c in columns:
            self.heading(c, text=c.capitalize())
