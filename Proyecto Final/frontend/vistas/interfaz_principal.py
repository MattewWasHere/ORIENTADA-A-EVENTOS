# NOTE: consecutivo is generated automatically; GUI should not input it.
import tkinter as tk
from tkinter import ttk, messagebox
from . import __name__ as _pkg  # ensure package context
from ..controladores.api_client import *
from ..controladores.backup import start_backup_thread, read_interval
from queue import Queue, Empty
from datetime import datetime, timedelta

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('IHEP - Inventario de Herramientas y Préstamos')
        self.geometry('1050x720')
        self.configure(bg='#2b2b2b')  # dark background
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2b2b2b')
        self.style.configure('TLabel', background='#2b2b2b', foreground='#e6e6e6', font=('Segoe UI',10))
        self.style.configure('Header.TLabel', font=('Segoe UI',14,'bold'), foreground='#ffffff', background='#2b2b2b')
        self.style.configure('Accent.TButton', font=('Segoe UI',10,'bold'), foreground='white', background='#44475a')
        self.create_widgets()
        self.status_q = Queue()
        self.stop_event, self.thread = start_backup_thread(self.status_q)
        self.backup_interval = read_interval()
        self.next_backup = datetime.utcnow() + timedelta(seconds=self.backup_interval)
        self.after(500, self.process_status)
        self.update_countdown()

    def create_widgets(self):
        top = ttk.Frame(self); top.pack(fill='x', padx=12, pady=8)
        ttk.Label(top, text='IHEP - Inventario de Herramientas y Préstamos', style='Header.TLabel').pack(side='left')
        self.status_frame = ttk.Frame(top); self.status_frame.pack(side='right')
        ttk.Label(self.status_frame, text='Backup:', style='TLabel').grid(row=0,column=0, sticky='e')
        self.backup_label = ttk.Label(self.status_frame, text='--', width=30, style='TLabel'); self.backup_label.grid(row=0,column=1, sticky='w', padx=6)
        ttk.Label(self.status_frame, text='Siguiente en:', style='TLabel').grid(row=1,column=0, sticky='e')
        self.count_label = ttk.Label(self.status_frame, text='--', width=15, style='TLabel'); self.count_label.grid(row=1,column=1, sticky='w', padx=6)

        self.notebook = ttk.Notebook(self); self.notebook.pack(fill='both', expand=True, padx=12, pady=8)
        self.v_h = VistaHerramientas(self.notebook); self.v_p = VistaPrestamos(self.notebook); self.v_b = VistaBusqueda(self.notebook, self.v_h, self.v_p)
        self.notebook.add(self.v_h, text='Herramientas'); self.notebook.add(self.v_p, text='Préstamos'); self.notebook.add(self.v_b, text='Búsqueda')

    def process_status(self):
        try:
            while True:
                item = self.status_q.get_nowait()
                tipo = item[0]
                if tipo == 'ok':
                    fname = item[1]; interval = item[2]
                    self.backup_label.config(text=f'Último: {fname}')
                    self.backup_interval = interval
                    self.next_backup = datetime.utcnow() + timedelta(seconds=interval)
                elif tipo == 'error':
                    self.backup_label.config(text=f'Error backup: {item[1][:40]}')
        except Empty:
            pass
        self.after(500, self.process_status)

    def update_countdown(self):
        remaining = int((self.next_backup - datetime.utcnow()).total_seconds())
        if remaining < 0: remaining = 0
        m, s = divmod(remaining, 60)
        self.count_label.config(text=f'{m:02d}:{s:02d}')
        self.after(1000, self.update_countdown)

    def on_close(self):
        try:
            self.stop_event.set(); self.thread.join(timeout=2)
        except: pass
        self.destroy()

class VistaHerramientas(ttk.Frame):
    def __init__(self, master):
        super().__init__(master); self.pack(fill='both', expand=True)
        self.create_form(); self.create_table(); self.load_herramientas()

    def create_form(self):
        frm = ttk.Frame(self); frm.pack(fill='x', padx=12, pady=8)
        ttk.Label(frm, text='Código:').grid(row=0,column=0, sticky='w')
        ttk.Label(frm, text='Nombre:').grid(row=1,column=0, sticky='w')
        ttk.Label(frm, text='Categoría:').grid(row=2,column=0, sticky='w')
        ttk.Label(frm, text='Ubicación:').grid(row=3,column=0, sticky='w')
        ttk.Label(frm, text='Estado:').grid(row=4,column=0, sticky='w')
        self.codigo = tk.StringVar(); self.nombre = tk.StringVar(); self.categoria = tk.StringVar(); self.ubicacion = tk.StringVar(); self.estado = tk.StringVar()
        ttk.Entry(frm, textvariable=self.codigo, width=30).grid(row=0,column=1, sticky='w')
        ttk.Entry(frm, textvariable=self.nombre, width=50).grid(row=1,column=1, sticky='w')
        ttk.Entry(frm, textvariable=self.categoria, width=30).grid(row=2,column=1, sticky='w')
        ttk.Entry(frm, textvariable=self.ubicacion, width=30).grid(row=3,column=1, sticky='w')
        ttk.Combobox(frm, textvariable=self.estado, values=['disponible','prestada','danada'], width=27).grid(row=4,column=1, sticky='w')
        btn_frame = ttk.Frame(frm); btn_frame.grid(row=5,column=0,columnspan=2, pady=8)
        ttk.Button(btn_frame, text='Guardar', style='Accent.TButton', command=self.guardar).grid(row=0,column=0, padx=4)
        ttk.Button(btn_frame, text='Editar', command=self.editar).grid(row=0,column=1, padx=4)
        ttk.Button(btn_frame, text='Eliminar', command=self.eliminar).grid(row=0,column=2, padx=4)

    def create_table(self):
        cols = ('codigo','nombre','categoria','ubicacion','estado')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=14)
        for c in cols:
            self.tree.heading(c, text=c.capitalize()); self.tree.column(c, width=140)
        self.tree.pack(fill='both', expand=True, padx=12, pady=8)

    def load_herramientas(self):
        try:
            data = get_herramientas()
            for i in self.tree.get_children(): self.tree.delete(i)
            for h in data:
                self.tree.insert('', 'end', values=(h.get('codigo'), h.get('nombre'), h.get('categoria'), h.get('ubicacion',''), h.get('estado','')))
        except Exception as e:
            messagebox.showerror('Error', f'No se pudieron cargar herramientas: {e}')

    def validar(self):
        if not self.codigo.get().strip(): messagebox.showwarning('Validación','Código es obligatorio'); return False
        if not self.nombre.get().strip(): messagebox.showwarning('Validación','Nombre es obligatorio'); return False
        if not self.categoria.get().strip(): messagebox.showwarning('Validación','Categoría es obligatoria'); return False
        if not self.estado.get().strip(): messagebox.showwarning('Validación','Estado es obligatorio'); return False
        return True

    def guardar(self):
        if not self.validar(): return
        payload = {'codigo': self.codigo.get().strip(),'nombre': self.nombre.get().strip(),'categoria': self.categoria.get().strip(),'ubicacion': self.ubicacion.get().strip(),'estado': self.estado.get().strip()}
        try:
            create_herramienta(payload); self.load_herramientas()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def editar(self):
        sel = self.tree.selection(); 
        if not sel: messagebox.showinfo('Info','Seleccione una herramienta'); return
        codigo = self.tree.item(sel[0])['values'][0]
        payload = {'codigo': codigo,'nombre': self.nombre.get().strip(),'categoria': self.categoria.get().strip(),'ubicacion': self.ubicacion.get().strip(),'estado': self.estado.get().strip()}
        try:
            update_herramienta(codigo, payload); self.load_herramientas()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def eliminar(self):
        sel = self.tree.selection()
        if not sel: messagebox.showinfo('Info','Seleccione una herramienta'); return
        codigo = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno('Confirmar','¿Eliminar herramienta?'):
            try:
                delete_herramienta(codigo); self.load_herramientas()
            except Exception as e:
                messagebox.showerror('Error', str(e))

class VistaPrestamos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master); self.pack(fill='both', expand=True)
        self.create_form(); self.create_table(); self.load_prestamos()

    def create_form(self):
        frm = ttk.Frame(self); frm.pack(fill='x', padx=12, pady=8)
        ttk.Label(frm, text='Consecutivo:').grid(row=0,column=0, sticky='w')
        ttk.Label(frm, text='Código Herramienta:').grid(row=1,column=0, sticky='w')
        ttk.Label(frm, text='Usuario:').grid(row=2,column=0, sticky='w')
        self.num = tk.StringVar(); self.hcod = tk.StringVar(); self.usuario = tk.StringVar()
        ttk.Entry(frm, textvariable=self.num, width=30).grid(row=0,column=1, sticky='w')
        ttk.Entry(frm, textvariable=self.hcod, width=30).grid(row=1,column=1, sticky='w')
        ttk.Entry(frm, textvariable=self.usuario, width=50).grid(row=2,column=1, sticky='w')
        btn_frame = ttk.Frame(frm); btn_frame.grid(row=3,column=0,columnspan=2, pady=8)
        ttk.Button(btn_frame, text='Registrar', style='Accent.TButton', command=self.registrar).grid(row=0,column=0, padx=4)
        ttk.Button(btn_frame, text='Devolver', command=self.devolver).grid(row=0,column=1, padx=4)
        ttk.Button(btn_frame, text='Eliminar', command=self.eliminar).grid(row=0,column=2, padx=4)

    def create_table(self):
        cols = ('consecutivo','herramienta_codigo','usuario','fecha_salida','fecha_prevista','fecha_devolucion')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=14)
        for c in cols:
            self.tree.heading(c, text=c.capitalize()); self.tree.column(c, width=130)
        self.tree.pack(fill='both', expand=True, padx=12, pady=8)

    def load_prestamos(self):
        try:
            data = get_prestamos()
            for i in self.tree.get_children(): self.tree.delete(i)
            for p in data:
                self.tree.insert('', 'end', values=(p.get('consecutivo'), p.get('herramienta_codigo'), p.get('usuario'), p.get('fecha_salida'), p.get('fecha_prevista'), p.get('fecha_devolucion')))
        except Exception as e:
            messagebox.showerror('Error', f'No se pudieron cargar préstamos: {e}')

    def validar(self):
        if not self.num.get().strip(): messagebox.showwarning('Validación','Consecutivo obligatorio'); return False
        if not self.hcod.get().strip(): messagebox.showwarning('Validación','Código herramienta obligatorio'); return False
        if not self.usuario.get().strip(): messagebox.showwarning('Validación','Usuario obligatorio'); return False
        return True

    def registrar(self):
        if not self.validar(): return
        try:
            herramientas = get_herramientas(); found = None
            for h in herramientas:
                if h.get('codigo') == self.hcod.get().strip():
                    found = h; break
            if not found:
                messagebox.showerror('Error','Herramienta no encontrada'); return
            if found.get('estado') != 'disponible':
                messagebox.showwarning('Validación','La herramienta no está disponible'); return
            payload = {'consecutivo': self.num.get().strip(), 'herramienta_codigo': self.hcod.get().strip(), 'usuario': self.usuario.get().strip(), 'fecha_salida': datetime.utcnow().isoformat()+'Z', 'fecha_prevista': datetime.utcnow().isoformat()+'Z'}
            create_prestamo(payload)
            found['estado'] = 'prestada'; update_herramienta(found['codigo'], found)
            self.load_prestamos()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def devolver(self):
        sel = self.tree.selection()
        if not sel: messagebox.showinfo('Info','Seleccione préstamo'); return
        num = self.tree.item(sel[0])['values'][0]
        try:
            payload = {'fecha_devolucion': datetime.utcnow().isoformat()+'Z'}
            update_prestamo(num, payload)
            for p in get_prestamos():
                if p.get('consecutivo') == num:
                    herr_code = p.get('herramienta_codigo')
                    herrs = get_herramientas()
                    for h in herrs:
                        if h.get('codigo') == herr_code:
                            h['estado'] = 'disponible'; update_herramienta(h['codigo'], h)
                            break
                    break
            self.load_prestamos()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def eliminar(self):
        sel = self.tree.selection()
        if not sel: messagebox.showinfo('Info','Seleccione préstamo'); return
        num = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno('Confirmar','¿Eliminar préstamo?'):
            try:
                delete_prestamo(num); self.load_prestamos()
            except Exception as e:
                messagebox.showerror('Error', str(e))

class VistaBusqueda(ttk.Frame):
    def __init__(self, master, vh, vp):
        super().__init__(master)
        self.vh = vh; self.vp = vp
        frm = ttk.Frame(self); frm.pack(fill='x', padx=12, pady=8)
        ttk.Label(frm, text='Término:').grid(row=0,column=0)
        self.term = tk.StringVar(); ttk.Entry(frm, textvariable=self.term, width=40).grid(row=0,column=1)
        ttk.Button(frm, text='Buscar', command=self.buscar).grid(row=0,column=2, padx=6)
        self.tree = ttk.Treeview(self, columns=('tipo','id','nombre','extra'), show='headings', height=16)
        for c in ('tipo','id','nombre','extra'): self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill='both', expand=True, padx=12, pady=8)

    def buscar(self):
        t = self.term.get().strip().lower()
        if not t: return
        try:
            herr = get_herramientas(); pres = get_prestamos(); res = []
            for h in herr:
                txt = (h.get('codigo','')+' '+h.get('nombre','')+' '+h.get('categoria','')).lower()
                if t in txt: res.append(('Herramienta', h.get('codigo'), h.get('nombre'), h.get('estado')))
            for p in pres:
                txt = (p.get('consecutivo','')+' '+p.get('herramienta_codigo','')+' '+p.get('usuario','')).lower()
                if t in txt: res.append(('Préstamo', p.get('consecutivo'), p.get('usuario'), p.get('herramienta_codigo')))
            for i in self.tree.get_children(): self.tree.delete(i)
            for r in res: self.tree.insert('', 'end', values=r)
        except Exception as e:
            messagebox.showerror('Error', str(e))

def iniciar_aplicacion():
    app = App(); app.protocol('WM_DELETE_WINDOW', app.on_close); app.mainloop()
