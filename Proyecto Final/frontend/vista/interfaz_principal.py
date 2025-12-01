
import tkinter as tk
from tkinter import ttk, messagebox
import threading, time, datetime, json, os
from tkcalendar import DateEntry
from frontend.modelos.herramienta_model import HerramientaModel
from frontend.modelos.prestamo_model import PrestamoModel

BACKUP_FILE = os.path.join(os.path.dirname(__file__), '..', 'backups', 'backup.json')

class InterfazPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('IHEP - Inventario y Préstamos (Entrega Final)')
        self.geometry('1200x720')
        self.configure(bg='#1f1f1f')

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Treeview', background='#2b2b2b', foreground='white', fieldbackground='#2b2b2b', rowheight=26)
        style.map('Treeview', background=[('selected', '#3a3a3a')])

        self.herr_model = HerramientaModel()
        self.pres_model = PrestamoModel()

        self._build_ui()

        # ensure backups dir exists
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'backups'), exist_ok=True)

        # start background threads
        threading.Thread(target=self._load_loop, daemon=True).start()
        threading.Thread(target=self._backup_loop, daemon=True).start()

    def _build_ui(self):
        nb = ttk.Notebook(self); nb.pack(fill='both', expand=True, padx=8, pady=8)
        self.tab_h = ttk.Frame(nb); self.tab_p = ttk.Frame(nb); self.tab_b = ttk.Frame(nb)
        nb.add(self.tab_h, text='Herramientas'); nb.add(self.tab_p, text='Préstamos'); nb.add(self.tab_b, text='Búsqueda')

        # Herramientas tab
        frm = ttk.Frame(self.tab_h); frm.pack(fill='x', padx=8, pady=8)
        cols_h = ('codigo','nombre','descripcion','cantidad','ubicacion','estado')
        self.h_vars = {c: tk.StringVar() for c in cols_h}
        for i,c in enumerate(cols_h):
            ttk.Label(frm, text=c.capitalize()+':').grid(row=i, column=0, sticky='e')
            ttk.Entry(frm, textvariable=self.h_vars[c]).grid(row=i, column=1, sticky='w')
        ttk.Button(frm, text='Guardar', command=self.guardar_h).grid(row=6,column=0)
        ttk.Button(frm, text='Eliminar', command=self.eliminar_h).grid(row=6,column=1)
        ttk.Button(frm, text='Limpiar', command=self.limpiar_h).grid(row=6,column=2)

        self.tree_h = ttk.Treeview(self.tab_h, columns=cols_h, show='headings', height=12)
        for c in cols_h:
            self.tree_h.heading(c, text=c.capitalize()); self.tree_h.column(c, width=160)
        self.tree_h.pack(fill='both', expand=True, padx=8, pady=6)
        self.tree_h.bind('<<TreeviewSelect>>', self.on_h_select)

        # Prestamos tab
        frm2 = ttk.Frame(self.tab_p); frm2.pack(fill='x', padx=8, pady=8)
        pcols = ('id','herramienta_codigo','persona_entrega','persona_recibe','fecha_entrega','fecha_prevista','fecha_devolucion','estado')
        self.p_vars = { 'herramienta_codigo': tk.StringVar(), 'persona_entrega': tk.StringVar(), 'persona_recibe': tk.StringVar() }
        ttk.Label(frm2, text='Herramienta Código:').grid(row=0,column=0); ttk.Entry(frm2,textvariable=self.p_vars['herramienta_codigo']).grid(row=0,column=1)
        ttk.Label(frm2, text='Persona entrega:').grid(row=1,column=0); ttk.Entry(frm2,textvariable=self.p_vars['persona_entrega']).grid(row=1,column=1)
        ttk.Label(frm2, text='Persona recibe:').grid(row=2,column=0); ttk.Entry(frm2,textvariable=self.p_vars['persona_recibe']).grid(row=2,column=1)
        ttk.Label(frm2, text='Fecha entrega:').grid(row=3,column=0); self.d_ent = DateEntry(frm2,date_pattern='yyyy-mm-dd'); self.d_ent.grid(row=3,column=1)
        ttk.Label(frm2, text='Fecha prevista:').grid(row=4,column=0); self.d_prev = DateEntry(frm2,date_pattern='yyyy-mm-dd'); self.d_prev.grid(row=4,column=1)
        ttk.Button(frm2, text='Registrar', command=self.registrar_p).grid(row=5,column=0)
        ttk.Button(frm2, text='Devolver', command=self.devolver_p).grid(row=5,column=1)
        ttk.Button(frm2, text='Limpiar', command=self.limpiar_p).grid(row=5,column=2)

        self.tree_p = ttk.Treeview(self.tab_p, columns=pcols, show='headings', height=10)
        for c in pcols:
            self.tree_p.heading(c, text=c.capitalize()); self.tree_p.column(c, width=140)
        self.tree_p.pack(fill='both', expand=True, padx=8, pady=6)
        self.tree_p.bind('<<TreeviewSelect>>', self.on_p_select)

        # Busqueda tab
        frm3 = ttk.Frame(self.tab_b); frm3.pack(fill='x', padx=8, pady=8)
        ttk.Label(frm3, text='Buscar:').grid(row=0,column=0); self.q = tk.StringVar(); ttk.Entry(frm3,textvariable=self.q,width=50).grid(row=0,column=1)
        ttk.Button(frm3, text='Buscar', command=self.buscar).grid(row=0,column=2)
        self.tree_b = ttk.Treeview(self.tab_b, columns=('tipo','valor','info'), show='headings', height=15)
        for c in ('tipo','valor','info'):
            self.tree_b.heading(c, text=c.capitalize()); self.tree_b.column(c, width=300)
        self.tree_b.pack(fill='both', expand=True, padx=8, pady=6)

    # -------------------- helpers and handlers --------------------
    def _load_loop(self):
        import requests, time
        # wait for backend a bit then poll
        for _ in range(10):
            try:
                requests.get('http://127.0.0.1:8000/api/herramientas/', timeout=1)
                break
            except Exception:
                time.sleep(1)
        self._listar_all()
        while True:
            time.sleep(5)
            self._listar_all()

    def _backup_loop(self):
        # save backup every 300 seconds (5 min)
        import time, json, os
        while True:
            try:
                herrs = self.herr_model.listar()
                pres = self.pres_model.listar()
                data = {'herramientas': herrs, 'prestamos': pres, 'ts': datetime.datetime.utcnow().isoformat()+'Z'}
                with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print('Backup error', e)
            time.sleep(300)

    def _listar_all(self):
        try:
            herrs = self.herr_model.listar()
            pres = self.pres_model.listar()
        except Exception as e:
            print('API error', e); return
        # fill herramientas
        self.tree_h.delete(*self.tree_h.get_children())
        for h in herrs:
            self.tree_h.insert('', 'end', values=(h.get('codigo'), h.get('nombre'), h.get('descripcion'), h.get('cantidad'), h.get('ubicacion'), h.get('estado')))
        # fill prestamos
        self.tree_p.delete(*self.tree_p.get_children())
        for p in pres:
            self.tree_p.insert('', 'end', values=(p.get('id'), p.get('herramienta_codigo'), p.get('persona_entrega'), p.get('persona_recibe'), p.get('fecha_entrega'), p.get('fecha_prevista'), p.get('fecha_devolucion'), p.get('estado')))

    def buscar(self):
        term = (self.q.get() or '').strip().lower()
        if not term:
            messagebox.showinfo('Buscar','Ingrese un término'); return
        results = []
        try:
            herrs = self.herr_model.listar(); pres = self.pres_model.listar()
        except Exception as e:
            messagebox.showerror('Error API', str(e)); return
        for h in herrs:
            if term in (h.get('codigo','') or '').lower() or term in (h.get('nombre','') or '').lower():
                results.append(('Herramienta', h.get('codigo'), h.get('nombre')))
        for p in pres:
            if term in (p.get('persona_recibe','') or '').lower() or term in (p.get('persona_entrega','') or '').lower():
                results.append(('Prestamo', p.get('id'), p.get('persona_recibe')))
        self.tree_b.delete(*self.tree_b.get_children())
        for r in results:
            self.tree_b.insert('', 'end', values=r)

    # UI interactions
    def on_h_select(self, event):
        sel = self.tree_h.selection()
        if not sel: return
        v = self.tree_h.item(sel[0])['values']
        keys = ('codigo','nombre','descripcion','cantidad','ubicacion','estado')
        for i,k in enumerate(keys):
            self.h_vars[k].set(v[i])

    def on_p_select(self, event):
        sel = self.tree_p.selection()
        if not sel: return
        v = self.tree_p.item(sel[0])['values']
        # populate form
        self.p_vars['herramienta_codigo'].set(v[1])
        self.p_vars['persona_entrega'].set(v[2])
        self.p_vars['persona_recibe'].set(v[3])
        try:
            if v[4]:
                self.d_ent.set_date(v[4][:10])
            if v[5]:
                self.d_prev.set_date(v[5][:10])
        except Exception:
            pass

    def guardar_h(self):
        data = {k: (self.h_vars[k].get() or '').strip() for k in self.h_vars}
        # validations
        if not data['codigo'] or not data['nombre'] or not data['cantidad']:
            messagebox.showwarning('Validación','Código, nombre y cantidad son obligatorios'); return
        # convert cantidad to int
        try:
            data['cantidad'] = int(data['cantidad'])
        except ValueError:
            messagebox.showwarning('Validación','Cantidad debe ser número'); return
        try:
            self.herr_model.crear(data)
            self._listar_all()
            messagebox.showinfo('OK','Herramienta guardada')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def eliminar_h(self):
        codigo = (self.h_vars['codigo'].get() or '').strip()
        if not codigo:
            messagebox.showwarning('Validación','Seleccione código'); return
        try:
            self.herr_model.eliminar(codigo)
            self._listar_all()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def limpiar_h(self):
        for k in self.h_vars: self.h_vars[k].set('')

    def registrar_p(self):
        data = {
            'herramienta_codigo': (self.p_vars['herramienta_codigo'].get() or '').strip(),
            'persona_entrega': (self.p_vars['persona_entrega'].get() or '').strip(),
            'persona_recibe': (self.p_vars['persona_recibe'].get() or '').strip(),
            'fecha_entrega': self.d_ent.get_date().strftime('%Y-%m-%dT00:00:00'),
            'fecha_prevista': self.d_prev.get_date().strftime('%Y-%m-%dT00:00:00'),
            'fecha_devolucion': None,
            'estado': 'activo'
        }
        if not data['herramienta_codigo'] or not data['persona_recibe']:
            messagebox.showwarning('Validación','Código y persona que recibe obligatorios'); return
        try:
            self.pres_model.crear(data)
            # update herramienta estado
            try:
                self.herr_model.actualizar_estado(data['herramienta_codigo'],'prestada')
            except Exception:
                pass
            self._listar_all()
            messagebox.showinfo('OK','Préstamo registrado')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def devolver_p(self):
        sel = self.tree_p.selection()
        if not sel:
            messagebox.showwarning('Validación','Seleccione préstamo'); return
        v = self.tree_p.item(sel[0])['values']
        pid = v[0]
        data = {'fecha_devolucion': datetime.date.today().strftime('%Y-%m-%dT00:00:00'), 'estado': 'cerrado'}
        try:
            self.pres_model.actualizar(pid, data)
            self.herr_model.actualizar_estado(v[1], 'disponible')
            self._listar_all()
            messagebox.showinfo('OK','Préstamo devuelto')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def limpiar_p(self):
        for k in self.p_vars: self.p_vars[k].set('')
