# frontend/vista/interfaz_principal.py
import threading
import time
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Importa los modelos/frontend controllers (deben existir)
from frontend.modelos.herramienta_model import HerramientaModel
from frontend.modelos.prestamo_model import PrestamoModel
from frontend.controladores.backup import BackupController


class InterfazPrincipal(tk.Tk):
    """
    Interfaz principal estilo oscuro (Theme C).
    Requisitos: frontend.modelos.herramienta_model HerramientaModel
                frontend.modelos.prestamo_model PrestamoModel
                frontend.controladores.backup BackupController (ejecutar_backup o hacer_backup)
    """

    BACKUP_INTERVAL = 300  # segundos (5 minutos)

    def __init__(self):
        super().__init__()
        self.title("IHEP — Inventario y Préstamos (Oscuro)")
        self.geometry("1200x760")
        self.configure(bg="#0f0f12")

        # modelos
        self.herr_model = HerramientaModel()
        self.pres_model = PrestamoModel()

        # backup controller (compatibilidad con métodos ejecutar_backup / hacer_backup)
        self.backup_ctrl = BackupController(self.herr_model, self.pres_model)

        # estado del hilo
        self._stop_event = threading.Event()
        self._next_backup_seconds = self.BACKUP_INTERVAL
        self._last_backup_path = None

        # estilos
        self._setup_styles()

        # construir UI
        self._build_ui()

        # iniciar hilo de backup
        threading.Thread(target=self._backup_loop, daemon=True).start()

        # cargar datos tras iniciar
        self.after(300, self._listar_herramientas)
        self.after(300, self._listar_prestamos)

    # -----------------------
    # estilos / tema oscuro
    # -----------------------
    def _setup_styles(self):
        style = ttk.Style(self)
        # For Windows, 'clam' works reasonably well
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # General widget colors
        style.configure("TFrame", background="#0f0f12")
        style.configure("TLabel", background="#0f0f12", foreground="#e6e6e6", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground="#ffffff", background="#0f0f12")
        style.configure("TButton", background="#1f2933", foreground="#e6e6e6", font=("Segoe UI", 10, "bold"),
                        padding=6)
        style.map("TButton", background=[("active", "#2b3340")])

        style.configure("Treeview", background="#101216", fieldbackground="#101216", foreground="#e6e6e6",
                        rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), foreground="#ffffff")

        # Smaller entry style fallback
        style.configure("TEntry", fieldbackground="#1a1a1a", foreground="#e6e6e6")

    # -----------------------
    # UI build
    # -----------------------
    def _build_ui(self):
        # Encabezado
        header = ttk.Frame(self)
        header.pack(fill="x", padx=12, pady=(12, 6))
        ttk.Label(header, text="IHEP — INVENTARIO & PRÉSTAMOS", style="Header.TLabel").pack(side="left")

        # Backup status / contador
        self.lbl_backup = ttk.Label(header, text="Respaldo: —", style="TLabel")
        self.lbl_backup.pack(side="right", padx=(0, 10))
        self.lbl_counter = ttk.Label(header, text="", style="TLabel")
        self.lbl_counter.pack(side="right", padx=(0, 8))

        # Notebook
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=8)

        # tabs
        self.tab_herr = ttk.Frame(nb)
        self.tab_pres = ttk.Frame(nb)
        self.tab_busq = ttk.Frame(nb)

        nb.add(self.tab_herr, text="Herramientas")
        nb.add(self.tab_pres, text="Préstamos")
        nb.add(self.tab_busq, text="Búsqueda")

        self._build_herramientas_tab()
        self._build_prestamos_tab()
        self._build_busqueda_tab()

    # -----------------------
    # Herramientas tab
    # -----------------------
    def _build_herramientas_tab(self):
        frm_top = ttk.Frame(self.tab_herr)
        frm_top.pack(fill="x", padx=8, pady=8)

        campos = ["Código", "Nombre", "Tipo", "Ubicación", "Estado"]
        self.h_vars = {c: tk.StringVar() for c in campos}

        for i, c in enumerate(campos):
            ttk.Label(frm_top, text=c).grid(row=i, column=0, sticky="e", padx=6, pady=4)
            ttk.Entry(frm_top, textvariable=self.h_vars[c], width=40).grid(row=i, column=1, sticky="w", padx=6)

        btn_guardar = ttk.Button(frm_top, text="Guardar", command=self._guardar_herramienta)
        btn_eliminar = ttk.Button(frm_top, text="Eliminar", command=self._eliminar_herramienta)
        btn_listar = ttk.Button(frm_top, text="Listar", command=self._listar_herramientas)

        btn_guardar.grid(row=6, column=0, pady=10)
        btn_eliminar.grid(row=6, column=1, sticky="w", padx=6)
        btn_listar.grid(row=6, column=1, sticky="e", padx=6)

        # Treeview herramientas
        cols = ("codigo", "nombre", "tipo", "ubicacion", "estado", "created_at")
        self.tree_h = ttk.Treeview(self.tab_herr, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree_h.heading(c, text=c.replace("_", " ").capitalize())
            self.tree_h.column(c, width=150 if c != "created_at" else 200)
        self.tree_h.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.tree_h.bind("<<TreeviewSelect>>", self._on_select_herramienta)

    def _on_select_herramienta(self, _event):
        sel = self.tree_h.focus()
        if not sel:
            return
        vals = self.tree_h.item(sel, "values")
        # column order: codigo, nombre, tipo, ubicacion, estado, created_at
        if not vals:
            return
        self.h_vars["Código"].set(vals[0])
        self.h_vars["Nombre"].set(vals[1])
        self.h_vars["Tipo"].set(vals[2])
        self.h_vars["Ubicación"].set(vals[3])
        self.h_vars["Estado"].set(vals[4])

    def _listar_herramientas(self):
        try:
            datos = self.herr_model.listar()
        except Exception as exc:
            messagebox.showerror("API error", f"No se pudo listar herramientas:\n{exc}")
            return
        self.tree_h.delete(*self.tree_h.get_children())
        # datos esperado: lista de dicts
        for h in datos:
            if isinstance(h, list) and len(h) > 0:
                # en caso de respuesta envolviendo
                h = h[0]
            self.tree_h.insert("", "end", values=(
                h.get("codigo", ""),
                h.get("nombre", ""),
                h.get("tipo", ""),
                h.get("ubicacion", "") or "",
                h.get("estado", ""),
                h.get("created_at", "")
            ))

    def _guardar_herramienta(self):
        data = {
            "codigo": self.h_vars["Código"].get().strip(),
            "nombre": self.h_vars["Nombre"].get().strip(),
            "tipo": self.h_vars["Tipo"].get().strip() or "General",
            "ubicacion": self.h_vars["Ubicación"].get().strip(),
            "estado": self.h_vars["Estado"].get().strip() or "disponible"
        }
        if not data["codigo"] or not data["nombre"]:
            messagebox.showwarning("Validación", "Código y Nombre son obligatorios")
            return
        try:
            # si existe en la vista -> update, sino create
            exists = False
            for item in self.tree_h.get_children():
                vals = self.tree_h.item(item, "values")
                if vals and vals[0] == data["codigo"]:
                    exists = True
                    break
            if exists:
                # actualizar por código
                self.herr_model.actualizar(data["codigo"], data)
            else:
                self.herr_model.crear(data)
            self._listar_herramientas()
            messagebox.showinfo("OK", "Herramienta guardada")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo guardar herramienta:\n{exc}")

    def _eliminar_herramienta(self):
        codigo = self.h_vars["Código"].get().strip()
        if not codigo:
            messagebox.showwarning("Validación", "Seleccione una herramienta para eliminar")
            return
        if not messagebox.askyesno("Confirmar", f"Eliminar herramienta {codigo}?"):
            return
        try:
            self.herr_model.eliminar(codigo)
            self._listar_herramientas()
            messagebox.showinfo("OK", "Herramienta eliminada")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo eliminar herramienta:\n{exc}")

    # -----------------------
    # Prestamos tab
    # -----------------------
    def _build_prestamos_tab(self):
        frm_top = ttk.Frame(self.tab_pres)
        frm_top.pack(fill="x", padx=8, pady=8)

        self.p_vars = {
            "herramienta_codigo": tk.StringVar(),
            "responsable": tk.StringVar(),
            "persona_entrega": tk.StringVar(),
            "persona_recibe": tk.StringVar()
        }

        # filas inputs
        ttk.Label(frm_top, text="Código Herramienta").grid(row=0, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm_top, textvariable=self.p_vars["herramienta_codigo"], width=30).grid(row=0, column=1, sticky="w")

        ttk.Label(frm_top, text="Responsable").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm_top, textvariable=self.p_vars["responsable"], width=30).grid(row=1, column=1, sticky="w")

        ttk.Label(frm_top, text="Persona Entrega").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm_top, textvariable=self.p_vars["persona_entrega"], width=30).grid(row=2, column=1, sticky="w")

        ttk.Label(frm_top, text="Persona Recibe").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm_top, textvariable=self.p_vars["persona_recibe"], width=30).grid(row=3, column=1, sticky="w")

        ttk.Label(frm_top, text="Fecha Entrega").grid(row=0, column=2, sticky="e", padx=6)
        self.fecha_entrega = DateEntry(frm_top, date_pattern="yyyy-mm-dd")
        self.fecha_entrega.grid(row=0, column=3, sticky="w", padx=6)

        ttk.Label(frm_top, text="Fecha Prevista").grid(row=1, column=2, sticky="e", padx=6)
        self.fecha_prevista = DateEntry(frm_top, date_pattern="yyyy-mm-dd")
        self.fecha_prevista.grid(row=1, column=3, sticky="w", padx=6)

        btn_registrar = ttk.Button(frm_top, text="Registrar préstamo", command=self._guardar_prestamo)
        btn_devolver = ttk.Button(frm_top, text="Registrar devolución", command=self._devolver_prestamo)
        btn_eliminar = ttk.Button(frm_top, text="Eliminar préstamo", command=self._eliminar_prestamo)

        btn_registrar.grid(row=4, column=0, pady=10)
        btn_devolver.grid(row=4, column=1)
        btn_eliminar.grid(row=4, column=2)

        # treeview prestamos
        cols = ("id", "herramienta_codigo", "responsable", "persona_entrega", "persona_recibe",
                "fecha_entrega", "fecha_prevista", "fecha_devolucion", "estado", "created_at")
        self.tree_p = ttk.Treeview(self.tab_pres, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree_p.heading(c, text=c.replace("_", " ").capitalize())
            self.tree_p.column(c, width=120 if c != "created_at" else 180)
        self.tree_p.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.tree_p.bind("<<TreeviewSelect>>", self._on_select_prestamo)

    def _on_select_prestamo(self, _event):
        sel = self.tree_p.focus()
        if not sel:
            return
        vals = self.tree_p.item(sel, "values")
        # columnas: id, herramienta_codigo, responsable, persona_entrega, persona_recibe, fecha_entrega, fecha_prevista, fecha_devolucion, estado, created_at
        if not vals:
            return
        self.p_vars["herramienta_codigo"].set(vals[1])
        self.p_vars["responsable"].set(vals[2])
        self.p_vars["persona_entrega"].set(vals[3])
        self.p_vars["persona_recibe"].set(vals[4])
        # si hay fecha_entrega / fecha_prevista se pueden poner en los DateEntry (si parsean)
        try:
            if vals[5]:
                dt = datetime.datetime.strptime(vals[5], "%Y-%m-%d")
                self.fecha_entrega.set_date(dt.date())
            if vals[6]:
                dt2 = datetime.datetime.strptime(vals[6], "%Y-%m-%d")
                self.fecha_prevista.set_date(dt2.date())
        except Exception:
            pass

    def _listar_prestamos(self):
        try:
            datos = self.pres_model.listar()
        except Exception as exc:
            messagebox.showerror("API error", f"No se pudo listar préstamos:\n{exc}")
            return
        self.tree_p.delete(*self.tree_p.get_children())
        for p in datos:
            if isinstance(p, list) and len(p) > 0:
                p = p[0]
            self.tree_p.insert("", "end", values=(
                p.get("id", ""),
                p.get("herramienta_codigo", ""),
                p.get("responsable", ""),
                p.get("persona_entrega", ""),
                p.get("persona_recibe", ""),
                p.get("fecha_entrega", "") or "",
                p.get("fecha_prevista", "") or "",
                p.get("fecha_devolucion", "") or "",
                p.get("estado", ""),
                p.get("created_at", "")
            ))

    def _guardar_prestamo(self):
        data = {
            "herramienta_codigo": self.p_vars["herramienta_codigo"].get().strip(),
            "responsable": self.p_vars["responsable"].get().strip(),
            "persona_entrega": self.p_vars["persona_entrega"].get().strip(),
            "persona_recibe": self.p_vars["persona_recibe"].get().strip(),
            "fecha_entrega": self.fecha_entrega.get_date().strftime("%Y-%m-%d"),
            "fecha_prevista": self.fecha_prevista.get_date().strftime("%Y-%m-%d"),
        }
        if not data["herramienta_codigo"] or not data["responsable"]:
            messagebox.showwarning("Validación", "Código herramienta y responsable son obligatorios")
            return
        try:
            resp = self.pres_model.crear(data)
            # si el backend creó correctamente, actualizar estado herramienta
            try:
                self.herr_model.actualizar_estado(data["herramienta_codigo"], "prestada")
            except Exception:
                pass
            self._listar_prestamos()
            self._listar_herramientas()
            messagebox.showinfo("OK", "Préstamo registrado")
        except Exception as exc:
            # si el modelo frontend lanza excepción con detalle del backend, muéstralo
            messagebox.showerror("Error al crear préstamo", str(exc))

    def _devolver_prestamo(self):
        sel = self.tree_p.focus()
        if not sel:
            messagebox.showwarning("Validación", "Seleccione un préstamo")
            return
        vals = self.tree_p.item(sel, "values")
        pid = vals[0]
        codigo = vals[1]
        fecha_devol = datetime.date.today().strftime("%Y-%m-%d")
        try:
            self.pres_model.actualizar(pid, {"fecha_devolucion": fecha_devol, "estado": "devuelto"})
            # cambiar estado herramienta
            try:
                self.herr_model.actualizar_estado(codigo, "disponible")
            except Exception:
                pass
            self._listar_prestamos()
            self._listar_herramientas()
            messagebox.showinfo("OK", "Devolución registrada")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo registrar la devolución:\n{exc}")

    def _eliminar_prestamo(self):
        sel = self.tree_p.focus()
        if not sel:
            messagebox.showwarning("Validación", "Seleccione un préstamo para eliminar")
            return
        vals = self.tree_p.item(sel, "values")
        pid = vals[0]
        if not messagebox.askyesno("Confirmar", f"Eliminar préstamo id={pid}?"):
            return
        try:
            self.pres_model.eliminar(pid)
            self._listar_prestamos()
            messagebox.showinfo("OK", "Préstamo eliminado")
        except Exception as exc:
            messagebox.showerror("Error", f"No se pudo eliminar préstamo:\n{exc}")

    # -----------------------
    # Busqueda tab
    # -----------------------
    def _build_busqueda_tab(self):
        frm = ttk.Frame(self.tab_busq)
        frm.pack(fill="x", padx=8, pady=8)
        ttk.Label(frm, text="Buscar (código/nombre/estado)").grid(row=0, column=0, padx=6)
        self.q_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.q_var, width=40).grid(row=0, column=1, padx=6)
        ttk.Button(frm, text="Buscar", command=self._buscar).grid(row=0, column=2, padx=6)

        # resultados
        cols = ("codigo", "nombre", "tipo", "ubicacion", "estado")
        self.tree_b = ttk.Treeview(self.tab_busq, columns=cols, show="headings")
        for c in cols:
            self.tree_b.heading(c, text=c.capitalize())
            self.tree_b.column(c, width=180)
        self.tree_b.pack(fill="both", expand=True, padx=8, pady=8)

    def _buscar(self):
        q = self.q_var.get().strip().lower()
        try:
            datos = self.herr_model.listar()
        except Exception as exc:
            messagebox.showerror("API error", f"No se pudo buscar:\n{exc}")
            return
        self.tree_b.delete(*self.tree_b.get_children())
        for h in datos:
            if isinstance(h, list) and len(h) > 0:
                h = h[0]
            if (q in (h.get("codigo", "").lower()) or
                    q in (h.get("nombre", "").lower()) or
                    q in (h.get("tipo", "").lower()) or
                    q in (h.get("estado", "").lower())):
                self.tree_b.insert("", "end", values=(
                    h.get("codigo", ""),
                    h.get("nombre", ""),
                    h.get("tipo", ""),
                    h.get("ubicacion", ""),
                    h.get("estado", "")
                ))

    # -----------------------
    # Backup loop (hilo)
    # -----------------------
    def _backup_loop(self):
        """
        Ejecuta backups periódicos en hilo aparte. Actualiza la UI con after().
        Intenta usar backup_ctrl.ejecutar_backup() o backup_ctrl.hacer_backup().
        """
        while not self._stop_event.is_set():
            try:
                # llamar al método disponible
                path = None
                if hasattr(self.backup_ctrl, "ejecutar_backup"):
                    path = self.backup_ctrl.ejecutar_backup()
                elif hasattr(self.backup_ctrl, "hacer_backup"):
                    path = self.backup_ctrl.hacer_backup()
                else:
                    # si no existe ninguno, intentamos ejecutar con nombre antiguo
                    if hasattr(self.backup_ctrl, "backup"):
                        path = self.backup_ctrl.backup()
                # actualizar UI desde hilo
                self._last_backup_path = path
                self._next_backup_seconds = self.BACKUP_INTERVAL
                self.after(0, lambda: self.lbl_backup.config(text=f"Respaldo: {path or '—'}"))
            except Exception as exc:
                # no queremos detener el hilo por errores; actualizamos la etiqueta
                self.after(0, lambda: self.lbl_backup.config(text=f"Respaldo error"))
                print("Error backup:", exc)
            # cuenta regresiva visual (cada segundo)
            for _ in range(self.BACKUP_INTERVAL):
                if self._stop_event.is_set():
                    break
                self._next_backup_seconds -= 1
                # actualiza contador (mm:ss)
                mins, secs = divmod(max(self._next_backup_seconds, 0), 60)
                text = f"Siguiente respaldo en {mins:02d}:{secs:02d}"
                self.after(0, lambda t=text: self.lbl_counter.config(text=t))
                time.sleep(1)
            # al terminar el intervalo, resetear contador para la próxima iteración
            self._next_backup_seconds = self.BACKUP_INTERVAL

    # -----------------------
    # cierre app (limpieza hilo)
    # -----------------------
    def destroy(self):
        # parar el hilo de backup
        self._stop_event.set()
        super().destroy()


def iniciar_aplicacion():
    app = InterfazPrincipal()
    app.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
