# frontend/vista/interfaz_principal.py
"""
Interfaz principal corregida y optimizada.

Características principales:
- Hilos para llamadas a la API (no bloquea UI)
- Backup en hilo con intervalo configurable por INTERVALO_BACKUP_SEG (env)
- Contador de respaldo bonito (muestra próxima ejecución / hora último respaldo)
- Animación suave: pulso en etiqueta de respaldo y entrada suave de tablas
- Botones de limpiar campos en pestañas Herramientas y Préstamos
- Manejo flexible de nombres de método de BackupController (ejecutar_backup / hacer_backup)
- Manejo de errores con mensajes al usuario
"""

import os
import threading
import time
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from queue import Queue, Empty

# Models / controllers (deben existir)
from frontend.modelos.herramienta_model import HerramientaModel
from frontend.modelos.prestamo_model import PrestamoModel
from frontend.controladores.backup import BackupController

# intervalo backup configurable por env var (segundos)
try:
    INTERVALO_BACKUP_SEG = int(os.getenv("INTERVALO_BACKUP_SEG", "300"))
except Exception:
    INTERVALO_BACKUP_SEG = 300


class InterfazPrincipal(tk.Tk):
    """Interfaz principal optimizada y con animaciones suaves."""

    def __init__(self):
        super().__init__()
        self.title("IHEP — Inventario y Préstamos")
        self.geometry("1200x760")
        self.configure(bg="#efefef")

        # --- modelos y controladores ---
        self.herr_model = HerramientaModel()
        self.pres_model = PrestamoModel()
        self.backup_ctrl = BackupController(self.herr_model, self.pres_model)

        # cola para comunicar resultados de hilos a UI
        self._q = Queue()

        # flags / sincronización
        self._list_lock = threading.Lock()
        self._stop_event = threading.Event()

        # estado de backup
        self._last_backup_time = None
        self._next_backup_seconds = INTERVALO_BACKUP_SEG

        # estilos y widgets
        self._setup_styles()
        self._build_ui()

        # iniciar hilo de backups (daemon)
        self._backup_thread = threading.Thread(target=self._backup_loop, daemon=True)
        self._backup_thread.start()

        # cargar datos (en hilo)
        self._debounce_timer = None
        self._load_all_async()

        # procesar cola periódicamente
        self.after(100, self._process_queue)

    # ----------------------
    # estilos
    # ----------------------
    def _setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # generales
        style.configure("TFrame", background="#efefef")
        style.configure("Header.TLabel", background="#efefef", font=("Segoe UI", 13, "bold"))
        style.configure("Sub.TLabel", background="#efefef", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Small.TButton", font=("Segoe UI", 9), padding=4)

        # Treeview look
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    # ----------------------
    # UI construction
    # ----------------------
    def _build_ui(self):
        # header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=12, pady=(12, 4))
        ttk.Label(header, text="IHEP — Inventario & Préstamos", style="Header.TLabel").pack(
            side="left", padx=(4, 0)
        )

        # backup status (no mostrar path crudo)
        self.lbl_backup = ttk.Label(header, text="Último respaldo: —", style="Sub.TLabel")
        self.lbl_backup.pack(side="right", padx=(0, 6))
        self.lbl_next = ttk.Label(header, text="", style="Sub.TLabel")
        self.lbl_next.pack(side="right", padx=(0, 10))

        # notebook
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=8)

        self.tab_herr = ttk.Frame(nb)
        self.tab_pres = ttk.Frame(nb)
        self.tab_busq = ttk.Frame(nb)

        nb.add(self.tab_herr, text="Herramientas")
        nb.add(self.tab_pres, text="Préstamos")
        nb.add(self.tab_busq, text="Búsqueda")

        self._build_herr_tab()
        self._build_pres_tab()
        self._build_busq_tab()

    # ----------------------
    # Herramientas tab
    # ----------------------
    def _build_herr_tab(self):
        frm = ttk.Frame(self.tab_herr)
        frm.pack(fill="x", padx=8, pady=8)

        labels = ["Código", "Nombre", "Tipo", "Ubicación", "Estado"]
        self.h_vars = {l: tk.StringVar() for l in labels}

        for i, label in enumerate(labels):
            ttk.Label(frm, text=label).grid(row=i, column=0, sticky="e", padx=6, pady=4)
            ttk.Entry(frm, textvariable=self.h_vars[label], width=40).grid(row=i, column=1, sticky="w")

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=len(labels), column=1, pady=8, sticky="w")
        ttk.Button(btn_frame, text="Guardar", style="Accent.TButton", command=self._guardar_herr).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Eliminar", style="Small.TButton", command=self._eliminar_herr).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Limpiar", style="Small.TButton", command=self._limpiar_herr).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Listar", style="Small.TButton", command=self._load_herramientas_async).pack(
            side="left", padx=4
        )

        # Treeview
        cols = ("codigo", "nombre", "tipo", "ubicacion", "estado", "created_at")
        self.tree_h = ttk.Treeview(self.tab_herr, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree_h.heading(c, text=c.replace("_", " ").capitalize())
            self.tree_h.column(c, width=150 if c != "created_at" else 200)
        self.tree_h.pack(fill="both", expand=True, padx=8, pady=(6, 8))
        self.tree_h.bind("<<TreeviewSelect>>", self._on_select_herr)

        # entrada suave: aplicar pequeña animación de aparición
        self.after(80, lambda: self._fade_in_widget(self.tree_h))

    def _on_select_herr(self, _event):
        sel = self.tree_h.focus()
        if not sel:
            return
        vals = self.tree_h.item(sel, "values")
        if not vals:
            return
        self.h_vars["Código"].set(vals[0])
        self.h_vars["Nombre"].set(vals[1])
        self.h_vars["Tipo"].set(vals[2])
        self.h_vars["Ubicación"].set(vals[3])
        self.h_vars["Estado"].set(vals[4])

    def _guardar_herr(self):
        data = {
            "codigo": self.h_vars["Código"].get().strip(),
            "nombre": self.h_vars["Nombre"].get().strip(),
            "tipo": self.h_vars["Tipo"].get().strip() or "General",
            "ubicacion": self.h_vars["Ubicación"].get().strip(),
            "estado": self.h_vars["Estado"].get().strip() or "disponible",
        }
        if not data["codigo"] or not data["nombre"]:
            messagebox.showwarning("Validación", "Código y Nombre son obligatorios")
            return

        # llamada en hilo para no bloquear UI
        def job():
            try:
                # update if exists in view
                exists = False
                for iid in self.tree_h.get_children():
                    v = self.tree_h.item(iid, "values")
                    if v and v[0] == data["codigo"]:
                        exists = True
                        break
                if exists:
                    self.herr_model.actualizar(data["codigo"], data)
                else:
                    self.herr_model.crear(data)
                self._q.put(("reload_herr", None))
                self._q.put(("msg", ("OK", "Herramienta guardada")))
            except Exception as exc:
                self._q.put(("msg", ("ERROR", f"No se pudo guardar herramienta:\n{exc}")))

        threading.Thread(target=job, daemon=True).start()

    def _eliminar_herr(self):
        codigo = self.h_vars["Código"].get().strip()
        if not codigo:
            messagebox.showwarning("Validación", "Seleccione una herramienta para eliminar")
            return
        if not messagebox.askyesno("Confirmar", f"Eliminar herramienta {codigo}?"):
            return

        def job():
            try:
                self.herr_model.eliminar(codigo)
                self._q.put(("reload_herr", None))
                self._q.put(("msg", ("OK", "Herramienta eliminada")))
            except Exception as exc:
                self._q.put(("msg", ("ERROR", f"No se pudo eliminar:\n{exc}")))

        threading.Thread(target=job, daemon=True).start()

    def _limpiar_herr(self):
        for k in self.h_vars:
            self.h_vars[k].set("")

    # ----------------------
    # Prestamos tab
    # ----------------------
    def _build_pres_tab(self):
        frm = ttk.Frame(self.tab_pres)
        frm.pack(fill="x", padx=8, pady=8)

        self.p_vars = {
            "herramienta_codigo": tk.StringVar(),
            "responsable": tk.StringVar(),
            "persona_entrega": tk.StringVar(),
            "persona_recibe": tk.StringVar(),
        }

        ttk.Label(frm, text="Código Herramienta").grid(row=0, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm, textvariable=self.p_vars["herramienta_codigo"], width=30).grid(row=0, column=1, sticky="w")

        ttk.Label(frm, text="Responsable").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm, textvariable=self.p_vars["responsable"], width=30).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Persona Entrega").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm, textvariable=self.p_vars["persona_entrega"], width=30).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Persona Recibe").grid(row=3, column=0, sticky="e", padx=6, pady=4)
        ttk.Entry(frm, textvariable=self.p_vars["persona_recibe"], width=30).grid(row=3, column=1, sticky="w")

        ttk.Label(frm, text="Fecha Entrega").grid(row=0, column=2, sticky="e", padx=6, pady=4)
        self.fecha_entrega = DateEntry(frm, date_pattern="yyyy-mm-dd")
        self.fecha_entrega.grid(row=0, column=3, sticky="w", padx=6)

        ttk.Label(frm, text="Fecha Prevista").grid(row=1, column=2, sticky="e", padx=6, pady=4)
        self.fecha_prevista = DateEntry(frm, date_pattern="yyyy-mm-dd")
        self.fecha_prevista.grid(row=1, column=3, sticky="w", padx=6)

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=4, column=0, columnspan=4, pady=8, sticky="w")
        ttk.Button(btn_frame, text="Registrar préstamo", style="Accent.TButton", command=self._guardar_pres).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Registrar devolución", style="Small.TButton", command=self._devolver_pres).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Eliminar préstamo", style="Small.TButton", command=self._eliminar_pres).pack(
            side="left", padx=4
        )
        ttk.Button(btn_frame, text="Limpiar", style="Small.TButton", command=self._limpiar_pres).pack(
            side="left", padx=4
        )

        # treeview prestamos
        cols = ("id", "herramienta_codigo", "responsable", "persona_entrega", "persona_recibe",
                "fecha_entrega", "fecha_prevista", "fecha_devolucion", "estado", "created_at")
        self.tree_p = ttk.Treeview(self.tab_pres, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree_p.heading(c, text=c.replace("_", " ").capitalize())
            self.tree_p.column(c, width=120 if c != "created_at" else 180)
        self.tree_p.pack(fill="both", expand=True, padx=8, pady=(6, 8))
        self.tree_p.bind("<<TreeviewSelect>>", self._on_select_pres)

        self.after(80, lambda: self._fade_in_widget(self.tree_p))

    def _on_select_pres(self, _event):
        sel = self.tree_p.focus()
        if not sel:
            return
        vals = self.tree_p.item(sel, "values")
        if not vals:
            return
        # columnas: id, herramienta_codigo, responsable, persona_entrega, persona_recibe, ...
        self.p_vars["herramienta_codigo"].set(vals[1])
        self.p_vars["responsable"].set(vals[2])
        self.p_vars["persona_entrega"].set(vals[3])
        self.p_vars["persona_recibe"].set(vals[4])
        # set date entries if present
        try:
            if vals[5]:
                d = datetime.datetime.strptime(vals[5], "%Y-%m-%d")
                self.fecha_entrega.set_date(d.date())
            if vals[6]:
                d2 = datetime.datetime.strptime(vals[6], "%Y-%m-%d")
                self.fecha_prevista.set_date(d2.date())
        except Exception:
            pass

    def _guardar_pres(self):
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

        def job():
            try:
                resp = self.pres_model.crear(data)
                # intentar actualizar estado herramienta (no bloquear)
                try:
                    self.herr_model.actualizar_estado(data["herramienta_codigo"], "prestada")
                except Exception:
                    pass
                self._q.put(("reload_all", None))
                self._q.put(("msg", ("OK", "Préstamo registrado")))
            except Exception as exc:
                # pasar detalle al hilo UI
                self._q.put(("msg", ("ERROR", f"No se pudo crear préstamo:\n{exc}")))

        threading.Thread(target=job, daemon=True).start()

    def _devolver_pres(self):
        sel = self.tree_p.focus()
        if not sel:
            messagebox.showwarning("Validación", "Seleccione un préstamo")
            return
        vals = self.tree_p.item(sel, "values")
        pid = vals[0]
        codigo = vals[1]
        fecha_devol = datetime.date.today().strftime("%Y-%m-%d")

        def job():
            try:
                # note: models expect 'fecha_devolucion' field name — unify with backend
                self.pres_model.actualizar(pid, {"fecha_devolucion": fecha_devol, "estado": "devuelto"})
                try:
                    self.herr_model.actualizar_estado(codigo, "disponible")
                except Exception:
                    pass
                self._q.put(("reload_all", None))
                self._q.put(("msg", ("OK", "Devolución registrada")))
            except Exception as exc:
                self._q.put(("msg", ("ERROR", f"No se pudo registrar devolución:\n{exc}")))

        threading.Thread(target=job, daemon=True).start()

    def _eliminar_pres(self):
        sel = self.tree_p.focus()
        if not sel:
            messagebox.showwarning("Validación", "Seleccione un préstamo para eliminar")
            return
        vals = self.tree_p.item(sel, "values")
        pid = vals[0]
        if not messagebox.askyesno("Confirmar", f"Eliminar préstamo id={pid}?"):
            return

        def job():
            try:
                self.pres_model.eliminar(pid)
                self._q.put(("reload_pres", None))
                self._q.put(("msg", ("OK", "Préstamo eliminado")))
            except Exception as exc:
                self._q.put(("msg", ("ERROR", f"No se pudo eliminar préstamo:\n{exc}")))

        threading.Thread(target=job, daemon=True).start()

    def _limpiar_pres(self):
        for k in self.p_vars:
            self.p_vars[k].set("")
        # reset date entries to today
        self.fecha_entrega.set_date(datetime.date.today())
        self.fecha_prevista.set_date(datetime.date.today())

    # ----------------------
    # Busqueda tab
    # ----------------------
    def _build_busq_tab(self):
        frm = ttk.Frame(self.tab_busq)
        frm.pack(fill="x", padx=8, pady=8)
        ttk.Label(frm, text="Buscar (código/nombre/tipo/estado)").grid(row=0, column=0, padx=6)
        self.q_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.q_var, width=40).grid(row=0, column=1, padx=6)
        ttk.Button(frm, text="Buscar", style="Small.TButton", command=self._buscar).grid(row=0, column=2, padx=6)

        # resultados
        cols = ("codigo", "nombre", "tipo", "ubicacion", "estado")
        self.tree_b = ttk.Treeview(self.tab_busq, columns=cols, show="headings")
        for c in cols:
            self.tree_b.heading(c, text=c.capitalize())
            self.tree_b.column(c, width=200)
        self.tree_b.pack(fill="both", expand=True, padx=8, pady=8)

    def _buscar(self):
        q = self.q_var.get().strip()
        if not q:
            messagebox.showinfo("Buscar", "Especifique al menos una letra o número para buscar")
            return

        # búsqueda asíncrona para no bloquear
        def job():
            try:
                datos = self.herr_model.listar()
                self._q.put(("search_results", (q, datos)))
            except Exception as exc:
                self._q.put(("msg", ("ERROR", f"No se pudo buscar:\n{exc}")))

        threading.Thread(target=job, daemon=True).start()

    # ----------------------
    # Carga / recarga (optimizada)
    # ----------------------
    def _load_all_async(self):
        """Carga herramientas y préstamos en paralelo, con debounce si se llama repetidamente."""
        # cancelar debounce si existe
        if self._debounce_timer:
            try:
                self.after_cancel(self._debounce_timer)
            except Exception:
                pass
        # programar ejecución en 200ms (debounce)
        self._debounce_timer = self.after(200, lambda: threading.Thread(target=self._load_all_job, daemon=True).start())

    def _load_all_job(self):
        """Job que carga ambas listas sin bloquear UI."""
        # obtain both lists concurrently
        results = {}

        def load_herr():
            try:
                results["herr"] = self.herr_model.listar()
            except Exception as e:
                results["herr_exc"] = e

        def load_pres():
            try:
                results["pres"] = self.pres_model.listar()
            except Exception as e:
                results["pres_exc"] = e

        t1 = threading.Thread(target=load_herr)
        t2 = threading.Thread(target=load_pres)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self._q.put(("load_results", results))

    def _load_herramientas_async(self):
        threading.Thread(target=self._load_herr_job, daemon=True).start()

    def _load_herr_job(self):
        try:
            datos = self.herr_model.listar()
            self._q.put(("herr_list", datos))
        except Exception as exc:
            self._q.put(("msg", ("ERROR", f"No se pudo listar herramientas:\n{exc}")))

    def _load_pres_async(self):
        threading.Thread(target=self._load_pres_job, daemon=True).start()

    def _load_pres_job(self):
        try:
            datos = self.pres_model.listar()
            self._q.put(("pres_list", datos))
        except Exception as exc:
            self._q.put(("msg", ("ERROR", f"No se pudo listar préstamos:\n{exc}")))

    # ----------------------
    # Backup loop (hilo)
    # ----------------------
    def _backup_loop(self):
        """Hilo daemon que ejecuta backups periódicamente y actualiza contador.
        No escribe ruta completa en la UI, solo la hora del último respaldo.
        """
        interval = INTERVALO_BACKUP_SEG or 300
        next_seconds = interval
        while not self._stop_event.is_set():
            try:
                # ejecutar backup (nombre flexible del método)
                path = None
                if hasattr(self.backup_ctrl, "ejecutar_backup"):
                    path = self.backup_ctrl.ejecutar_backup()
                elif hasattr(self.backup_ctrl, "hacer_backup"):
                    path = self.backup_ctrl.hacer_backup()
                elif hasattr(self.backup_ctrl, "backup"):
                    path = self.backup_ctrl.backup()

                now = datetime.datetime.now()
                self._last_backup_time = now
                # push to UI: do not expose path, only time
                self._q.put(("backup_done", now))
            except Exception as exc:
                # report error but do not stop
                self._q.put(("msg", ("ERROR", f"Error backup: {exc}")))
            # countdown with 1s steps
            for i in range(interval):
                if self._stop_event.is_set():
                    break
                secs = interval - i
                self._q.put(("backup_countdown", secs))
                time.sleep(1)

    # ----------------------
    # Cola -> UI processing
    # ----------------------
    def _process_queue(self):
        """Procesa mensajes de la cola puestos por los hilos."""
        try:
            while True:
                item = self._q.get_nowait()
                if not item:
                    continue
                key, payload = item
                if key == "load_results":
                    r = payload
                    if "herr_exc" in r:
                        messagebox.showerror("API error", f"No se pudo listar herramientas:\n{r['herr_exc']}")
                    if "pres_exc" in r:
                        messagebox.showerror("API error", f"No se pudo listar préstamos:\n{r['pres_exc']}")
                    if "herr" in r:
                        self._populate_tree_h(r["herr"])
                    if "pres" in r:
                        self._populate_tree_p(r["pres"])
                elif key == "herr_list":
                    self._populate_tree_h(payload)
                elif key == "pres_list":
                    self._populate_tree_p(payload)
                elif key == "reload_herr":
                    self._load_herr_job()
                elif key == "reload_pres":
                    self._load_pres_job()
                elif key == "reload_all":
                    self._load_all_async()
                elif key == "search_results":
                    q, datos = payload
                    self._populate_search(q, datos)
                elif key == "backup_done":
                    t = payload
                    self.lbl_backup.config(text=f"Último respaldo: {t.strftime('%Y-%m-%d %H:%M:%S')}")
                    # trigger pulse animation (suave)
                    self._pulse_label(self.lbl_backup, times=2)
                elif key == "backup_countdown":
                    secs = payload
                    mins, s = divmod(secs, 60)
                    self.lbl_next.config(text=f"Siguiente: {mins:02d}:{s:02d}")
                elif key == "msg":
                    typ, txt = payload
                    if typ == "OK":
                        # mostrar info pero no molestar: usar showinfo
                        messagebox.showinfo("OK", txt)
                    else:
                        messagebox.showerror(typ, txt)
                elif key == "reload_herr":
                    self._load_herr_job()
                self._q.task_done()
        except Empty:
            pass
        # volver a revisar cola
        self.after(100, self._process_queue)

    # ----------------------
    # population helpers
    # ----------------------
    def _populate_tree_h(self, datos):
        self.tree_h.delete(*self.tree_h.get_children())
        for h in datos:
            # backend may return datetimes; keep safe get
            self.tree_h.insert("", "end", values=(
                h.get("codigo", ""),
                h.get("nombre", ""),
                h.get("tipo", "") or h.get("categoria", ""),
                h.get("ubicacion", "") or "",
                h.get("estado", ""),
                h.get("created_at", "") or "",
            ))

    def _populate_tree_p(self, datos):
        self.tree_p.delete(*self.tree_p.get_children())
        for p in datos:
            self.tree_p.insert("", "end", values=(
                p.get("id", ""),
                p.get("herramienta_codigo", "") or p.get("codigo", ""),
                p.get("responsable", ""),
                p.get("persona_entrega", ""),
                p.get("persona_recibe", ""),
                p.get("fecha_entrega", "") or "",
                p.get("fecha_prevista", "") or "",
                p.get("fecha_devolucion", "") or "",
                p.get("estado", ""),
                p.get("created_at", "") or "",
            ))

    def _populate_search(self, q, datos):
        self.tree_b.delete(*self.tree_b.get_children())
        ql = q.lower()
        for h in datos:
            if isinstance(h, list) and len(h) > 0:
                h = h[0]
            code = (h.get("codigo", "") or "").lower()
            name = (h.get("nombre", "") or "").lower()
            tipo = (h.get("tipo", "") or h.get("categoria", "") or "").lower()
            estado = (h.get("estado", "") or "").lower()
            if ql in code or ql in name or ql in tipo or ql in estado:
                self.tree_b.insert("", "end", values=(
                    h.get("codigo", ""),
                    h.get("nombre", ""),
                    h.get("tipo", "") or h.get("categoria", ""),
                    h.get("ubicacion", "") or "",
                    h.get("estado", ""),
                ))

    # ----------------------
    # util animations
    # ----------------------
    def _fade_in_widget(self, widget, steps=8, delay=25):
        """Aparición simple: ajusta alfa mediante background alternado (simulación)."""
        # note: Tkinter doesn't support widget alpha easily; we simulate tiny delays for 'soft' load
        for i in range(steps):
            self.after(i * delay, lambda: widget.update())

    def _pulse_label(self, label, times=3, period=300):
        """Pulso suave cambiando el color de texto por breves instantes."""
        def pulse_once(count):
            if count <= 0:
                label.config(foreground="black")
                return
            # cambiar a color 'acento' y volver
            label.config(foreground="#0B7CFF")
            self.after(int(period / 2), lambda: label.config(foreground="black"))
            self.after(period, lambda: pulse_once(count - 1))

        pulse_once(times)

    # ----------------------
    # cierre / limpieza
    # ----------------------
    def destroy(self):
        # indicar al hilo que pare
        self._stop_event.set()
        super().destroy()


# ----------------------
# ejecutar
# ----------------------
def iniciar_aplicacion():
    app = InterfazPrincipal()
    app.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()
