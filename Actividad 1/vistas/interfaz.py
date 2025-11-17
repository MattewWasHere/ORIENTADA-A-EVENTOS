import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno
import re
from datetime import datetime

class InterfazPrincipal():

    def mostrar_interfaz():
        root = tk.Tk()
        root.title("Registro Estudiante")
        root.geometry("400x300")
        root.resizable(False, False)
        root.columnconfigure(1, weight=1)

        # 🔹 VARIABLES (todas las necesarias)
        root.var_nombre = tk.StringVar()
        root.var_edad = tk.StringVar()
        root.var_correo = tk.StringVar()
        root.var_fecha = tk.StringVar()

        root.err_nombre = tk.StringVar()
        root.err_edad = tk.StringVar()
        root.err_correo = tk.StringVar()
        root.err_fecha = tk.StringVar()

        # 🔹 CAMPOS Y ETIQUETAS
        tk.Label(root, text="Nombre").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        entry_nombre = tk.Entry(root, textvariable=root.var_nombre)
        entry_nombre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(root, textvariable=root.err_nombre, fg="red").grid(row=1, column=1, sticky="w")

        tk.Label(root, text="Edad").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        entry_edad = tk.Entry(root, textvariable=root.var_edad)
        entry_edad.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(root, textvariable=root.err_edad, fg="red").grid(row=3, column=1, sticky="w")

        tk.Label(root, text="Correo Electrónico").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        entry_correo = tk.Entry(root, textvariable=root.var_correo)
        entry_correo.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(root, textvariable=root.err_correo, fg="red").grid(row=5, column=1, sticky="w")

        tk.Label(root, text="Fecha Matrícula (YYYY-MM-DD)").grid(row=6, column=0, sticky="e", padx=10, pady=5)
        entry_fecha = tk.Entry(root, textvariable=root.var_fecha)
        entry_fecha.grid(row=6, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(root, textvariable=root.err_fecha, fg="red").grid(row=7, column=1, sticky="w")

        # 🔹 BOTONES
        tk.Button(root, text="Guardar", command=lambda: InterfazPrincipal.enviar(root)).grid(row=8, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(root, text="Eliminar Campos", command=lambda: InterfazPrincipal.limpiar(root)).grid(row=8, column=1, padx=10, pady=10, sticky="ew")

        # 🔹 BINDINGS
        entry_nombre.bind("<FocusOut>", lambda e: InterfazPrincipal.val_nombre(root))
        entry_edad.bind("<FocusOut>", lambda e: InterfazPrincipal.val_edad(root))
        entry_correo.bind("<FocusOut>", lambda e: InterfazPrincipal.val_correo(root))
        entry_fecha.bind("<FocusOut>", lambda e: InterfazPrincipal.val_fecha(root))

        entry_nombre.bind("<Return>", lambda e: InterfazPrincipal.enviar(root))
        entry_edad.bind("<Return>", lambda e: InterfazPrincipal.enviar(root))
        entry_correo.bind("<Return>", lambda e: InterfazPrincipal.enviar(root))
        entry_fecha.bind("<Return>", lambda e: InterfazPrincipal.enviar(root))

        # 🔹 CONFIRMACIÓN DE CIERRE
        root.protocol("WM_DELETE_WINDOW", lambda: InterfazPrincipal.confirmar_cierre(root))
        root.mainloop()

    # 🔹 VALIDACIONES
    def val_nombre(root):
        txt = root.var_nombre.get().strip()
        if txt == "":
            root.err_nombre.set("El nombre es obligatorio")
            return False
        elif not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", txt):
            root.err_nombre.set("Solo letras y espacios")
            return False
        root.err_nombre.set("")
        return True

    def val_edad(root):
        txt = root.var_edad.get().strip()
        if txt == "":
            root.err_edad.set("La edad es obligatoria")
            return False
        if not txt.isdigit():
            root.err_edad.set("Debe ser numérica")
            return False
        num = int(txt)
        if not (0 <= num <= 120):
            root.err_edad.set("Edad fuera de rango (0–120)")
            return False
        root.err_edad.set("")
        return True

    def val_correo(root):
        txt = root.var_correo.get().strip()
        if txt == "":
            root.err_correo.set("El correo es obligatorio")
            return False
        if not re.match(r"[^@]+@[^@]+\.[^@]+", txt):
            root.err_correo.set("Correo inválido")
            return False
        root.err_correo.set("")
        return True

    def val_fecha(root):
        txt = root.var_fecha.get().strip()
        if txt == "":
            root.err_fecha.set("La fecha es obligatoria")
            return False
        try:
            datetime.strptime(txt, "%Y-%m-%d")
            root.err_fecha.set("")
            return True
        except ValueError:
            root.err_fecha.set("Formato inválido (YYYY-MM-DD)")
            return False

    # 🔹 ENVÍO Y LIMPIEZA
    def enviar(root):
        ok = all([
            InterfazPrincipal.val_nombre(root),
            InterfazPrincipal.val_edad(root),
            InterfazPrincipal.val_correo(root),
            InterfazPrincipal.val_fecha(root)
        ])
        if not ok:
            messagebox.showerror("Errores", "Por favor, corrija los campos con errores")
            return
        messagebox.showinfo("Éxito", "Datos guardados correctamente")

    def limpiar(root):
        for var, err in [
            (root.var_nombre, root.err_nombre),
            (root.var_edad, root.err_edad),
            (root.var_correo, root.err_correo),
            (root.var_fecha, root.err_fecha),
        ]:
            var.set("")
            err.set("")

    def confirmar_cierre(root):
        if askyesno("Confirmar", "¿Desea cerrar la aplicación?"):
            root.destroy()

 


