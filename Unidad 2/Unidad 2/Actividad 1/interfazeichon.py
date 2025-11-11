import tkinter as tk
import re
from tkinter.messagebox import askyesno
from tkinter import messagebox
from datetime import datetime

root = tk.Tk()
root.title("Registro de Estudiantes")
root.geometry("400x400")
root.resizable(0,0)
root.config(padx=5, pady=20)


def usuario_sale():
    if askyesno("Salir de la aplicación", "¿Estás seguro que quieres cerrar la aplicación?"):
        root.destroy()

VAL_NOMBRE = re.compile(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$")
VAL_CORREO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

def limpiar_campos_texto():
    for var, err in [
        (var_nombre, err_nombre),
        (var_apellido, err_apellido),
        (var_correo, err_correo),
        (var_fecha_matricula, err_fecha_matricula)
    ]:
        var.set("")
        err.set("")

def val_nombre() -> bool:
    txt = var_nombre.get()
    if txt == "":
        err_nombre.set("")
        return True
    if VAL_NOMBRE.match(txt):
        err_nombre.set("")
        return True
    err_nombre.set("Solo se permiten letras y espacios")
    return False

def val_apellido() -> bool:
    txt = var_apellido.get()
    if txt == "":
        err_apellido.set("")
        return True
    if VAL_NOMBRE.match(txt):
        err_apellido.set("")
        return True
    err_apellido.set("Solo se permiten letras y espacios")
    return False

def val_correo() -> bool:
    txt = var_correo.get()
    if txt == "":
        err_correo.set("")
        return True
    if VAL_CORREO.match(txt):
        err_correo.set("")
        return True
    err_correo.set("Formato de correo inválido")
    return False

def val_fecha_matricula() -> bool:
    txt = var_fecha_matricula.get().strip()
    if txt == "":
        err_fecha_matricula.set("")
        return True
    try:
        datetime.strptime(txt, "%Y-%m-%d")
        err_fecha_matricula.set("")
        return True
    except ValueError:
        err_fecha_matricula.set("Fecha inválida. Use el formato YYYY-MM-DD")
        return False

def enviar():
    ok = all([
        val_nombre(),
        val_apellido(),
        val_correo(),
        val_fecha_matricula(),
    ])

    obligatorios = [
        (var_nombre.get().strip() != "", err_nombre, "El nombre es obligatorio."),
        (var_apellido.get().strip() != "", err_apellido, "El apellido es obligatorio."),
        (var_correo.get().strip() != "", err_correo, "El correo es obligatorio."),
        (var_fecha_matricula.get().strip() != "", err_fecha_matricula, "La fecha de matrícula es obligatoria."),
    ]
    for lleno, err_var, msg in obligatorios:
        if not lleno and err_var.get() == "":
            err_var.set(msg)
            ok = False

    if not ok:
        messagebox.showerror("Errores de validación", "Por favor corrija los campos marcados en rojo.")
        return

    messagebox.showinfo("Éxito", "¡Estudiante registrado correctamente!")

var_nombre = tk.StringVar()
var_apellido = tk.StringVar()
var_correo = tk.StringVar()
var_fecha_matricula = tk.StringVar()

err_nombre = tk.StringVar()
err_apellido = tk.StringVar()
err_correo = tk.StringVar()
err_fecha_matricula = tk.StringVar()


tk.Label(root, text="Nombre").grid(row=0, column=0, pady=(0, 20), sticky="w")
entry_nombre = tk.Entry(root, textvariable=var_nombre)
entry_nombre.grid(row=0, column=1, padx=(170, 0), pady=(0, 20), sticky="e")
tk.Label(textvariable=err_nombre, fg="#c1121f").grid(row=1, column=1, sticky="w", pady=(0,6))

tk.Label(root, text="Apellido").grid(row=2, column=0, pady=(0, 20), sticky="w")
entry_apellido = tk.Entry(root, textvariable=var_apellido)
entry_apellido.grid(row=2, column=1, pady=(0, 20), padx=(170, 0))
tk.Label(textvariable=err_apellido, fg="#c1121f").grid(row=3, column=1, sticky="w", pady=(0,6))

tk.Label(root, text="Correo Electrónico").grid(row=4, column=0, pady=(0, 20), sticky="w")
entry_correo = tk.Entry(root, textvariable=var_correo)
entry_correo.grid(row=4, column=1, pady=(0, 20), padx=(170, 0))
tk.Label(textvariable=err_correo, fg="#c1121f").grid(row=5, column=1, sticky="w", pady=(0,6))

tk.Label(root, text="Fecha de Matrícula").grid(row=6, column=0, pady=(0, 20), sticky="w")
entry_fecha_matricula = tk.Entry(root, textvariable=var_fecha_matricula)
entry_fecha_matricula.grid(row=6, column=1, pady=(0, 20), padx=(170, 0))
tk.Label(textvariable=err_fecha_matricula, fg="#c1121f").grid(row=7, column=1, sticky="w", pady=(0,6))

frame_botones = tk.Frame(root)
frame_botones.grid(row=8, column=0, columnspan=2, pady=(20,0))

btn_registrar = tk.Button(frame_botones, 
                         text="Registrar Estudiante",
                         command=enviar,
                         bg="#4CAF50",  # Verde
                         fg="white",
                         width=20,
                         height=2)
btn_registrar.grid(row=0, column=0, padx=10)

btn_limpiar = tk.Button(frame_botones, 
                       text="Limpiar",
                       command=limpiar_campos_texto,
                       bg="#f44336",  # Rojo
                       fg="white",
                       width=20,
                       height=2)
btn_limpiar.grid(row=0, column=1, padx=10)

root.geometry("600x450")

entry_nombre.bind("<KeyRelease>", lambda e: val_nombre())
entry_apellido.bind("<KeyRelease>", lambda e: val_apellido())
entry_correo.bind("<KeyRelease>", lambda e: val_correo())
entry_fecha_matricula.bind("<KeyRelease>", lambda e: val_fecha_matricula())

root.protocol("WM_DELETE_WINDOW", usuario_sale)

root.mainloop()