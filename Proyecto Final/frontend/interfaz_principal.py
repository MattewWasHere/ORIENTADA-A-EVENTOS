import os
import threading
import time
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from frontend.modelos.herramienta import HerramientaModel
from frontend.modelos.prestamos import PrestamoModel
from frontend.controladores.backup import BackupController


class InterfazPrincipal(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("IHEP - Inventario de Herramientas y Préstamos")
        self.geometry("1000x700")

        self.herr_model = HerramientaModel()
        self.pres_model = PrestamoModel()

        self.backup_ctrl = BackupController(self.herr_model, self.pres_model)
        self._stop_event = threading.Event()
        threading.Thread(target=self._backup_loop, daemon=True).start()

        self._build_ui()

        self.after(1000, self._listar_herramientas)
        self.after(1000, self._listar_prestamos)

    # ========================= UI =========================

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        self.tab_herr = ttk.Frame(nb)
        self.tab_pres = ttk.Frame(nb)
        self.tab_busq = ttk.Frame(nb)

        nb.add(self.tab_herr, text="Herramientas")
        nb.add(self.tab_pres, text="Préstamos")
        nb.add(self.tab_busq, text="Búsqueda")

        self._build_herramientas()
        self._build_prestamos()
        self._build_busqueda()

    # ================= HERRAMIENTAS =================

    def _build_herramientas(self):
        frm = ttk.Frame(self.tab_herr)
        frm.pack(fill="x", padx=8, pady=8)

        campos = ["Código", "Nombre", "Categoría", "Ubicación", "Estado"]
        self.h_vars = {k: tk.StringVar() for k in campos}

        for i, campo in enumerate(campos):
            ttk.Label(frm, text=campo).grid(row=i, column=0, sticky="e")
            ttk.Entry(frm, textvariable=self.h_vars[campo]).grid(row=i, column=1)

        ttk.Button(frm, text="Guardar", command=self._guardar_herramienta).grid(row=6, column=0)
        ttk.Button(frm, text="Eliminar", command=self._eliminar_herramienta).grid(row=6, column=1)
        ttk.Button(frm, text="Listar", command=self._listar_herramientas).grid(row=6, column=2)

        self.tree_h = ttk.Treeview(
            self.tab_herr,
            columns=("codigo", "nombre", "tipo", "ubicacion", "estado"),
            show="headings"
        )

        for c in ("codigo", "nombre", "tipo", "ubicacion", "estado"):
            self.tree_h.heading(c, text=c.capitalize())
            self.tree_h.column(c, width=160)

        self.tree_h.pack(fill="both", expand=True)

    def _normalizar_item(self, item):
        if isinstance(item, list) and len(item) > 0:
            item = item[0]
        if not isinstance(item, dict):
            return {}
        return item

    def _listar_herramientas(self):
        datos = self.herr_model.listar()
        self.tree_h.delete(*self.tree_h.get_children())

        for h in datos:
            h = self._normalizar_item(h)
            self.tree_h.insert("", "end", values=(
                h.get("codigo", ""),
                h.get("nombre", ""),
                h.get("tipo", ""),
                h.get("ubicacion", ""),
                h.get("estado", "")
            ))

    def _guardar_herramienta(self):
        data = {
            "codigo": self.h_vars["Código"].get(),
            "nombre": self.h_vars["Nombre"].get(),
            "tipo": self.h_vars["Categoría"].get(),
            "ubicacion": self.h_vars["Ubicación"].get(),
            "estado": self.h_vars["Estado"].get() or "disponible"
        }

        if not data["codigo"] or not data["nombre"]:
            messagebox.showwarning("Validación", "Código y nombre son obligatorios")
            return

        self.herr_model.crear(data)
        self._listar_herramientas()

    def _eliminar_herramienta(self):
        codigo = self.h_vars["Código"].get()
        if not codigo:
            return
        self.herr_model.eliminar(codigo)
        self._listar_herramientas()

    # ================= PRÉSTAMOS =================

    def _build_prestamos(self):
        frm = ttk.Frame(self.tab_pres)
        frm.pack(fill="x", padx=8, pady=8)

        self.p_vars = {
            "Herramienta Código": tk.StringVar(),
            "Responsable": tk.StringVar()
        }

        ttk.Label(frm, text="Herramienta Código").grid(row=0, column=0)
        ttk.Entry(frm, textvariable=self.p_vars["Herramienta Código"]).grid(row=0, column=1)

        ttk.Label(frm, text="Responsable").grid(row=1, column=0)
        ttk.Entry(frm, textvariable=self.p_vars["Responsable"]).grid(row=1, column=1)

        ttk.Label(frm, text="Fecha Salida").grid(row=2, column=0)
        self.fecha_salida = DateEntry(frm, date_pattern="yyyy-mm-dd")
        self.fecha_salida.grid(row=2, column=1)

        ttk.Label(frm, text="Fecha Esperada").grid(row=3, column=0)
        self.fecha_prevista = DateEntry(frm, date_pattern="yyyy-mm-dd")
        self.fecha_prevista.grid(row=3, column=1)

        ttk.Button(frm, text="Registrar", command=self._guardar_prestamo).grid(row=4, column=0)
        ttk.Button(frm, text="Devolver", command=self._devolver_prestamo).grid(row=4, column=1)

        self.tree_p = ttk.Treeview(
            self.tab_pres,
            columns=("consecutivo", "codigo", "usuario", "salida", "prevista", "devolucion"),
            show="headings"
        )

        for c in ("consecutivo", "codigo", "usuario", "salida", "prevista", "devolucion"):
            self.tree_p.heading(c, text=c.capitalize())
            self.tree_p.column(c, width=150)

        self.tree_p.pack(fill="both", expand=True)

    def _generar_consecutivo(self):
        return f"P-{int(time.time())}"  

    def _guardar_prestamo(self):
        herramienta_codigo = self.p_vars["Herramienta Código"].get()
        usuario = self.p_vars["Responsable"].get()

        if not herramienta_codigo or not usuario:
            messagebox.showwarning("Error", "Complete todos los campos")
            return

        data = {
            "consecutivo": self._generar_consecutivo(),
            "herramienta_codigo": herramienta_codigo,
            "usuario": usuario,
            "fecha_salida": self.fecha_salida.get_date().strftime("%Y-%m-%d"),
            "fecha_prevista": self.fecha_prevista.get_date().strftime("%Y-%m-%d"),
            "fecha_devolucion": None
        }
        print(data)

        if not self.pres_model.crear(data):
            messagebox.showerror("Error", "No se pudo registrar el préstamo")
            return

        self.herr_model.actualizar_estado(herramienta_codigo, "prestada")

        self._listar_prestamos()
        self._listar_herramientas()

    def _devolver_prestamo(self):
        seleccion = self.tree_p.focus()
        if not seleccion:
            return

        valores = self.tree_p.item(seleccion, "values")
        consecutivo = valores[0]
        codigo = valores[1]

        data = {
            "fecha_devolucion": datetime.date.today().strftime("%Y-%m-%d")
        }

        self.pres_model.actualizar(consecutivo, data)
        self.herr_model.actualizar_estado(codigo, "disponible")

        self._listar_prestamos()
        self._listar_herramientas()

    def _listar_prestamos(self):
        datos = self.pres_model.listar()
        self.tree_p.delete(*self.tree_p.get_children())

        for p in datos:
            p = self._normalizar_item(p)
            self.tree_p.insert("", "end", values=(
                p.get("consecutivo", ""),
                p.get("herramienta_codigo", ""),
                p.get("usuario", ""),
                p.get("fecha_salida", ""),
                p.get("fecha_prevista", ""),
                p.get("fecha_devolucion", "")
            ))

    # ================= BÚSQUEDA =================

    def _build_busqueda(self):
        frm = ttk.Frame(self.tab_busq)
        frm.pack(fill="x", padx=8, pady=8)

        ttk.Label(frm, text="Buscar:").grid(row=0, column=0)
        self.q_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.q_var).grid(row=0, column=1)
        ttk.Button(frm, text="Buscar", command=self._buscar).grid(row=0, column=2)

        self.tree_b = ttk.Treeview(
            self.tab_busq,
            columns=("codigo", "nombre", "estado"),
            show="headings"
        )

        for c in ("codigo", "nombre", "estado"):
            self.tree_b.heading(c, text=c.capitalize())
            self.tree_b.column(c, width=200)

        self.tree_b.pack(fill="both", expand=True)

    def _buscar(self):
        q = self.q_var.get().lower()
        datos = self.herr_model.listar()
        self.tree_b.delete(*self.tree_b.get_children())

        for h in datos:
            h = self._normalizar_item(h)
            if q in h.get("codigo", "").lower() or q in h.get("nombre", "").lower():
                self.tree_b.insert("", "end", values=(
                    h.get("codigo", ""),
                    h.get("nombre", ""),
                    h.get("estado", "")
                ))

    # ================= BACKUP =================

    def _backup_loop(self):
        while not self._stop_event.is_set():
            try:
                self.backup_ctrl.ejecutar_backup()
            except Exception as e:
                print("Error backup:", e)
            time.sleep(60)


def iniciar_aplicacion():
    app = InterfazPrincipal()
    app.mainloop()
