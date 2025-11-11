import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno
import re
from datetime import datetime

RE_NOMBRE = re.compile(r"^[A-Za-z ]+$")
RE_EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

class RegistroEstudiante(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro Estudiante")
        self.geometry("400x300")
        self.resizable(False, False)

        self.var_nombre = tk.StringVar()
        self.var_edad = tk.StringVar()
        self.var_correo = tk.StringVar()
        self.var_fecha = tk.StringVar()

        self.err_nombre = tk.StringVar()
        self.err_edad = tk.StringVar()
        self.err_correo = tk.StringVar()
        self.err_fecha = tk.StringVar()

        self.columnconfigure(1, weight=1)

        tk.Label(self, text="Nombre").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        entry_nombre = tk.Entry(self, textvariable=self.var_nombre)
        entry_nombre.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self, textvariable=self.err_nombre, fg="red").grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Edad").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        entry_edad = tk.Entry(self, textvariable=self.var_edad)
        entry_edad.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self, textvariable=self.err_edad, fg="red").grid(row=3, column=1, sticky="w")

        tk.Label(self, text="Correo Electrónico").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        entry_correo = tk.Entry(self, textvariable=self.var_correo)
        entry_correo.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self, textvariable=self.err_correo, fg="red").grid(row=5, column=1, sticky="w")

        tk.Label(self, text="Fecha Matrícula (YYYY-MM-DD)").grid(row=6, column=0, sticky="e", padx=10, pady=5)
        entry_fecha = tk.Entry(self, textvariable=self.var_fecha)
        entry_fecha.grid(row=6, column=1, sticky="ew", padx=10, pady=5)
        tk.Label(self, textvariable=self.err_fecha, fg="red").grid(row=7, column=1, sticky="w")

        tk.Button(self, text="Guardar", command=self.enviar).grid(row=8, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(self, text="Eliminar Campos", command=self.limpiar).grid(row=8, column=1, padx=10, pady=10, sticky="ew")

        """
        Bindings de eventos FocusOut y Return para validaciones y envío
        usando lambda para evitar pasar el evento como argumento
        El FocusOut tiene como funcion validar al salir del entry
        El Return tiene como funcion enviar los datos al presionar Enter
        """
        
        entry_nombre.bind("<FocusOut>", lambda e: self.val_nombre())
        entry_edad.bind("<FocusOut>", lambda e: self.val_edad())
        entry_correo.bind("<FocusOut>", lambda e: self.val_correo())
        entry_fecha.bind("<FocusOut>", lambda e: self.val_fecha())
        entry_nombre.bind("<Return>", lambda e: self.enviar())
        entry_edad.bind("<Return>", lambda e: self.enviar())
        entry_correo.bind("<Return>", lambda e: self.enviar())
        entry_fecha.bind("<Return>", lambda e: self.enviar())


        """ 
        El Self.protocol sirve como confirmación al cerrar ventana
        usando el ejemplo visto en clase
        """
        
        self.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)

    def val_nombre(self):
        txt = self.var_nombre.get().strip()
        if txt == "":
            self.err_nombre.set("El nombre es obligatorio")
            return False
        if RE_NOMBRE.match(txt):
            self.err_nombre.set("")
            return True
        self.err_nombre.set("Solo letras y espacios")
        return False

    def val_edad(self):
        txt = self.var_edad.get().strip()
        if txt == "":
            self.err_edad.set("La edad es obligatoria")
            return False
        if not txt.isdigit():
            self.err_edad.set("Debe ser numérica")
            return False
        num = int(txt)
        if not (0 <= num <= 120):
            self.err_edad.set("Edad fuera de rango (0–120)")
            return False
        self.err_edad.set("")
        return True

    def val_correo(self):
        txt = self.var_correo.get().strip()
        if txt == "":
            self.err_correo.set("El correo es obligatorio")
            return False
        if RE_EMAIL.match(txt):
            self.err_correo.set("")
            return True
        self.err_correo.set("Correo inválido")
        return False

    def val_fecha(self):
        txt = self.var_fecha.get().strip()
        if txt == "":
            self.err_fecha.set("La fecha es obligatoria")
            return False
        try:
            datetime.strptime(txt, "%Y-%m-%d")
            self.err_fecha.set("")
            return True
        except ValueError:
            self.err_fecha.set("Formato inválido (YYYY-MM-DD)")
            return False

    def enviar(self):
        ok = all([self.val_nombre(), self.val_edad(), self.val_correo(), self.val_fecha()])
        if not ok:
            messagebox.showerror("Errores", "Los campos vacíos deben ser rellenados")
            return
        messagebox.showinfo("Éxito", "Datos guardados correctamente")

    def limpiar(self):
        for var, err in [
            (self.var_nombre, self.err_nombre),
            (self.var_edad, self.err_edad),
            (self.var_correo, self.err_correo),
            (self.var_fecha, self.err_fecha),
        ]:
            var.set("")
            err.set("")
    
    def confirmar_cierre(self):
        if askyesno("Confirmar", "¿Desea cerrar la aplicación?"):
            self.destroy()
 

if __name__ == "__main__":
    RegistroEstudiante().mainloop()
