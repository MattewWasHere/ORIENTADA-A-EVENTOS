import tkinter as tk
from tkinter import ttk, messagebox
from ..controladores.comunicacion import obtener_herramientas, obtener_prestamos

class VistaBusqueda(tk.Frame):
    def __init__(self, master, vista_h, vista_p):
        super().__init__(master)
        self.vista_h = vista_h; self.vista_p = vista_p
        frm = tk.Frame(self); frm.pack(fill='x', padx=10, pady=6)
        tk.Label(frm, text='Término de búsqueda:').grid(row=0,column=0)
        self.term = tk.StringVar()
        tk.Entry(frm, textvariable=self.term).grid(row=0,column=1)
        tk.Button(frm, text='Buscar', command=self.buscar).grid(row=0,column=2)
        self.tree = ttk.Treeview(self, columns=('tipo','id','nombre','extra'), show='headings', height=20)
        for c in ('tipo','id','nombre','extra'): self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill='both', expand=True, padx=10, pady=6)

    def buscar(self):
        t = self.term.get().strip().lower()
        if not t: return
       
        try:
            herramientas = obtener_herramientas()
            prestamos = obtener_prestamos()
            resultados = []
            for h in herramientas:
                if t in (h.get('codigo','').lower() + h.get('nombre','').lower() + h.get('tipo','').lower()):
                    resultados.append(('Herramienta', h.get('codigo'), h.get('nombre'), h.get('estado')))
            for p in prestamos:
                if t in (p.get('consecutivo','').lower() + p.get('herramienta_codigo','').lower() + p.get('usuario','').lower()):
                    resultados.append(('Préstamo', p.get('consecutivo'), p.get('usuario'), p.get('herramienta_codigo')))
            for i in self.tree.get_children(): self.tree.delete(i)
            for r in resultados:
                self.tree.insert('', 'end', values=r)
        except Exception as e:
            messagebox.showerror('Error', str(e))
