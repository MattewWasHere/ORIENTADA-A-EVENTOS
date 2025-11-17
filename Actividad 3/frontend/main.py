import tkinter as tk
from tkinter import ttk, messagebox
import requests
import re

# URL del backend Django
API_URL = "http://127.0.0.1:8000/api/estudiantes/"

class EstudianteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Estudiantes")
        self.root.geometry("700x500")

        # Campos del formulario
        tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(root)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Apellido:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_apellido = tk.Entry(root)
        self.entry_apellido.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Correo:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_correo = tk.Entry(root)
        self.entry_correo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Fecha de matrícula (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_fecha = tk.Entry(root)
        self.entry_fecha.grid(row=3, column=1, padx=10, pady=5)

        # Botones
        self.btn_agregar = tk.Button(root, text="Agregar", command=self.agregar_estudiante)
        self.btn_agregar.grid(row=4, column=0, padx=10, pady=10)

        self.btn_actualizar = tk.Button(root, text="Actualizar", command=self.actualizar_estudiante, state=tk.DISABLED)
        self.btn_actualizar.grid(row=4, column=1, padx=10, pady=10)

        self.btn_eliminar = tk.Button(root, text="Eliminar", command=self.eliminar_estudiante, state=tk.DISABLED)
        self.btn_eliminar.grid(row=4, column=2, padx=10, pady=10)

        # Tabla
        columnas = ("id", "nombre", "apellido", "correo", "fecha_matricula")
        self.tabla = ttk.Treeview(root, columns=columnas, show="headings", height=15)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120)
        self.tabla.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_estudiante)

        # Cargar datos iniciales
        self.cargar_estudiantes()

    def validar_datos(self, nombre, apellido, correo, fecha):
        """Valida los campos antes de enviar al backend"""
        if not nombre or not apellido or not correo or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False

        if not nombre.isalpha() or not apellido.isalpha():
            messagebox.showerror("Error", "Nombre y Apellido solo deben contener letras.")
            return False

        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", correo):
            messagebox.showerror("Error", "El correo electrónico no tiene un formato válido.")
            return False

        return True

    def cargar_estudiantes(self):
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                for row in self.tabla.get_children():
                    self.tabla.delete(row)
                for estudiante in response.json():
                    self.tabla.insert("", "end", values=(
                        estudiante["id"],
                        estudiante["nombre"],
                        estudiante["apellido"],
                        estudiante["correo"],
                        estudiante["fecha_matricula"]
                    ))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor:\n{e}")

    def agregar_estudiante(self):
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        correo = self.entry_correo.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not self.validar_datos(nombre, apellido, correo, fecha):
            return

        data = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "fecha_matricula": fecha
        }

        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 201:
                messagebox.showinfo("Éxito", "Estudiante agregado correctamente.")
                self.cargar_estudiantes()
                # Limpiar formulario y deshabilitar botones de actualizar/eliminar
                self.entry_nombre.delete(0, tk.END)
                self.entry_apellido.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_fecha.delete(0, tk.END)
                try:
                    self.btn_actualizar.config(state=tk.DISABLED)
                    self.btn_eliminar.config(state=tk.DISABLED)
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", f"No se pudo agregar el estudiante.\n{response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor:\n{e}")

    def seleccionar_estudiante(self, event):
        item = self.tabla.focus()
        if not item:
            return
        valores = self.tabla.item(item, "values")
        self.id_seleccionado = valores[0]
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])
        self.entry_apellido.insert(0, valores[2])
        self.entry_correo.insert(0, valores[3])
        self.entry_fecha.insert(0, valores[4])

        # Habilitar botones de actualizar y eliminar cuando hay una selección
        try:
            self.btn_actualizar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)
        except Exception:
            pass

    def actualizar_estudiante(self):
        try:
            estudiante_id = self.id_seleccionado
        except AttributeError:
            messagebox.showwarning("Aviso", "Seleccione un estudiante de la tabla para actualizar.")
            return

        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        correo = self.entry_correo.get().strip()
        fecha = self.entry_fecha.get().strip()

        if not self.validar_datos(nombre, apellido, correo, fecha):
            return

        data = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "fecha_matricula": fecha
        }

        try:
            response = requests.put(f"{API_URL}{estudiante_id}/", json=data)
            if response.status_code == 200:
                messagebox.showinfo("Éxito", "Estudiante actualizado correctamente.")
                self.cargar_estudiantes()
                # Limpiar formulario y deshabilitar botones
                self.entry_nombre.delete(0, tk.END)
                self.entry_apellido.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_fecha.delete(0, tk.END)
                try:
                    del self.id_seleccionado
                except Exception:
                    pass
                try:
                    self.btn_actualizar.config(state=tk.DISABLED)
                    self.btn_eliminar.config(state=tk.DISABLED)
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", f"No se pudo actualizar el estudiante.\n{response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor:\n{e}")

    def eliminar_estudiante(self):
        try:
            estudiante_id = self.id_seleccionado
        except AttributeError:
            messagebox.showwarning("Aviso", "Seleccione un estudiante de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este estudiante?")
        if not confirmar:
            return

        try:
            response = requests.delete(f"{API_URL}{estudiante_id}/")
            if response.status_code == 204:
                messagebox.showinfo("Éxito", "Estudiante eliminado correctamente.")
                self.cargar_estudiantes()
                # Limpiar formulario y deshabilitar botones
                self.entry_nombre.delete(0, tk.END)
                self.entry_apellido.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_fecha.delete(0, tk.END)
                try:
                    del self.id_seleccionado
                except Exception:
                    pass
                try:
                    self.btn_actualizar.config(state=tk.DISABLED)
                    self.btn_eliminar.config(state=tk.DISABLED)
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el estudiante.\n{response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo conectar con el servidor:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EstudianteApp(root)
    root.mainloop()
