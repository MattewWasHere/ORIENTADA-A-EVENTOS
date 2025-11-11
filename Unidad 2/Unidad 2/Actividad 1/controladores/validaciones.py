import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re

VAL_NOMBRE = re.compile(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$")
VAL_CORREO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

class Validaciones:
    def __init__(self, variables, errores):
        self.variables = variables
        self.errores = errores

    def val_nombre(self) -> bool:
        txt = self.variables['nombre'].get()
        if txt == "":
            self.errores['nombre'].set("")
            return True
        if VAL_NOMBRE.match(txt):
            self.errores['nombre'].set("")
            return True
        self.errores['nombre'].set("Solo se permiten letras y espacios")
        return False

    def val_apellido(self) -> bool:
        txt = self.variables['apellido'].get()
        if txt == "":
            self.errores['apellido'].set("")
            return True
        if VAL_NOMBRE.match(txt):
            self.errores['apellido'].set("")
            return True
        self.errores['apellido'].set("Solo se permiten letras y espacios")
        return False

    def val_correo(self) -> bool:
        txt = self.variables['correo'].get()
        if txt == "":
            self.errores['correo'].set("")
            return True
        if VAL_CORREO.match(txt):
            self.errores['correo'].set("")
            return True
        self.errores['correo'].set("Formato de correo inválido")
        return False

    def val_fecha_matricula(self) -> bool:
        txt = self.variables['fecha_matricula'].get().strip()
        if txt == "":
            self.errores['fecha_matricula'].set("")
            return True
        try:
            datetime.strptime(txt, "%Y-%m-%d")
            self.errores['fecha_matricula'].set("")
            return True
        except ValueError:
            self.errores['fecha_matricula'].set("Fecha inválida. Use el formato YYYY-MM-DD")
            return False
        
    def enviar(self):
        # Validación de campos obligatorios
        obligatorios = [
            ('nombre', "El nombre es obligatorio"),
            ('apellido', "El apellido es obligatorio"),
            ('correo', "El correo es obligatorio"),
            ('fecha_matricula', "La fecha de matrícula es obligatoria")
        ]

        for campo, mensaje in obligatorios:
            if self.variables[campo].get().strip() == "":
                self.errores[campo].set(mensaje)
                return False

        # Ejecuta todas las validaciones
        ok = all([
            self.val_nombre(),
            self.val_apellido(),
            self.val_correo(),
            self.val_fecha_matricula()
        ])

        if not ok:
            messagebox.showerror("Errores de validación", "Por favor corrija los campos marcados en rojo.")
            return False

        messagebox.showinfo("Éxito", "¡Estudiante registrado correctamente!")
        return True

    def limpiar_campos_texto(self):
        for var in self.variables.values():
            var.set("")
        for err in self.errores.values():
            err.set("")