import tkinter as tk
from tkinter import ttk
from datetime import datetime

""" Variables globales para widgets (en lugar de atributos de clase)"""
notebook = None
tab_herramientas = None
tree_herramientas = None
entry_codigo = None
entry_nombre = None
entry_categoria = None
entry_ubicacion = None
entry_estado = None
entry_created_at = None
entry_updated_at = None
lbl_error = None

tab_prestamos = None
tree_prestamos = None

tab_busqueda = None
tree_busqueda = None


def setup_app(root):
    global notebook, tab_herramientas, tab_prestamos, tab_busqueda
    root.title("IHEP - Inventario de Herramientas y Préstamos")
    root.geometry("800x600")

    # Crear pestañas
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Pestaña Herramientas
    tab_herramientas = ttk.Frame(notebook)
    notebook.add(tab_herramientas, text="Herramientas")
    setup_tab_herramientas(root)

    # Pestaña Préstamos
    tab_prestamos = ttk.Frame(notebook)
    notebook.add(tab_prestamos, text="Préstamos")
    setup_tab_prestamos(root)

    # Pestaña Búsqueda
    tab_busqueda = ttk.Frame(notebook)
    notebook.add(tab_busqueda, text="Búsqueda")
    setup_tab_busqueda(root)


def setup_tab_herramientas(root):
    global tree_herramientas, entry_codigo, entry_nombre, entry_categoria, entry_ubicacion, entry_estado
    global entry_created_at, entry_updated_at, lbl_error

    # Formulario
    form_frame = tk.Frame(tab_herramientas)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Código:").grid(row=0, column=0, padx=5, pady=5)
    entry_codigo = tk.Entry(form_frame)
    entry_codigo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
    entry_nombre = tk.Entry(form_frame)
    entry_nombre.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Categoría:").grid(row=2, column=0, padx=5, pady=5)
    entry_categoria = tk.Entry(form_frame)
    entry_categoria.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Ubicación:").grid(row=3, column=0, padx=5, pady=5)
    entry_ubicacion = tk.Entry(form_frame)
    entry_ubicacion.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Estado:").grid(row=4, column=0, padx=5, pady=5)
    entry_estado = tk.Entry(form_frame)
    entry_estado.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Created_at:").grid(row=5, column=0, padx=5, pady=5)
    entry_created_at = tk.Entry(form_frame)
    entry_created_at.insert(0, datetime.now().isoformat())
    entry_created_at.config(state="disabled")  # Solo lectura
    entry_created_at.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Updated_at:").grid(row=6, column=0, padx=5, pady=5)
    entry_updated_at = tk.Entry(form_frame)
    entry_updated_at.insert(0, datetime.now().isoformat())
    entry_updated_at.config(state="disabled")
    entry_updated_at.grid(row=6, column=1, padx=5, pady=5)

    # Etiqueta de error
    lbl_error = tk.Label(form_frame, text="", fg="red", font=("Arial", 9, "bold"))
    lbl_error.grid(row=7, column=0, columnspan=2, pady=5)

    btn_guardar = tk.Button(form_frame, text="Guardar", command=guardar_herramienta)
    btn_guardar.grid(row=8, column=0, columnspan=2, pady=10)

    # Treeview
    columns = ("código", "nombre", "categoría", "ubicación", "estado", "created_at", "updated_at")
    tree_herramientas = ttk.Treeview(tab_herramientas, columns=columns, show="headings")
    for col in columns:
        tree_herramientas.heading(col, text=col.capitalize())
    tree_herramientas.pack(expand=True, fill="both", padx=10, pady=10)

    # Botones
    btn_agregar = tk.Button(tab_herramientas, text="Agregar Herramienta", command=agregar_herramienta)
    btn_agregar.pack(side=tk.LEFT, padx=10)
    btn_editar = tk.Button(tab_herramientas, text="Editar", command=editar_herramienta)
    btn_editar.pack(side=tk.LEFT, padx=10)
    btn_eliminar = tk.Button(tab_herramientas, text="Eliminar", command=eliminar_herramienta)
    btn_eliminar.pack(side=tk.LEFT, padx=10)


def guardar_herramienta():
    global lbl_error
    codigo = entry_codigo.get().strip()
    nombre = entry_nombre.get().strip()
    categoria = entry_categoria.get().strip()
    ubicacion = entry_ubicacion.get().strip()
    estado = entry_estado.get().strip()

    # Validaciones visuales
    if not all([codigo, nombre, categoria, ubicacion, estado]):
        lbl_error.config(text=" Todos los campos son obligatorios.")
        return

    if not codigo.isalnum():
        lbl_error.config(text=" El código solo debe contener letras y números.")
        return

    if not nombre.replace(" ", "").isalpha():
        lbl_error.config(text=" El nombre solo debe contener letras.")
        return

    if not categoria.replace(" ", "").isalpha():
        lbl_error.config(text=" La categoría solo debe contener letras.")
        return

    if not ubicacion.replace(" ", "").isalnum():
        lbl_error.config(text=" La ubicación debe contener letras o números válidos.")
        return

    if not estado.replace(" ", "").isalpha():
        lbl_error.config(text=" El estado solo debe contener letras.")
        return

    lbl_error.config(text="")  # limpiar error si todo está bien

    # Agregar a la tabla
    tree_herramientas.insert("", tk.END, values=(codigo, nombre, categoria, ubicacion, estado,
                                                 entry_created_at.get(), entry_updated_at.get()))
    limpiar_formulario()
    lbl_error.config(text="✔ Herramienta registrada correctamente.", fg="green")


def limpiar_formulario():
    entry_codigo.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)
    entry_ubicacion.delete(0, tk.END)
    entry_estado.delete(0, tk.END)


def setup_tab_prestamos(root):
    global tree_prestamos
    lbl = tk.Label(tab_prestamos, text="Formulario de Préstamos aquí")
    lbl.pack(pady=10)

    columns = ("número", "herramienta_código", "responsable", "fecha_salida", "fecha_esperada", "fecha_devolución")
    tree_prestamos = ttk.Treeview(tab_prestamos, columns=columns, show="headings")
    for col in columns:
        tree_prestamos.heading(col, text=col.capitalize())
    tree_prestamos.pack(expand=True, fill="both", padx=10, pady=10)

    btn_agregar = tk.Button(tab_prestamos, text="Agregar Préstamo", command=agregar_prestamo)
    btn_agregar.pack(side=tk.LEFT, padx=10)


def setup_tab_busqueda(root):
    global tree_busqueda
    lbl = tk.Label(tab_busqueda, text="Formulario de Búsqueda unificada aquí")
    lbl.pack(pady=10)

    tree_busqueda = ttk.Treeview(tab_busqueda, columns=("tipo", "detalles"), show="headings")
    tree_busqueda.heading("tipo", text="Tipo")
    tree_busqueda.heading("detalles", text="Detalles")
    tree_busqueda.pack(expand=True, fill="both", padx=10, pady=10)

    btn_buscar = tk.Button(tab_busqueda, text="Buscar", command=buscar)
    btn_buscar.pack(pady=10)


def agregar_herramienta():
    limpiar_formulario()


def editar_herramienta():
    print("Editar seleccionada")


def eliminar_herramienta():
    print("Eliminar seleccionada")


def agregar_prestamo():
    print("Abrir formulario de préstamo con validación de disponibilidad")


def buscar():
    print("Ejecutar búsqueda")


if __name__ == "__main__":
    root = tk.Tk()
    setup_app(root)
    root.mainloop()


