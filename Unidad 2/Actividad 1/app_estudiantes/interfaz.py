import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import django, os, sys

# Ajustar path para permitir ejecutar desde la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'registro_estudiante.settings')
django.setup()

from app_estudiantes.views import registrar_estudiante, listar_estudiantes

class InterfazEstudiantes:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Estudiantes")
        self.root.geometry("420x340")
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_cierre)

        tk.Label(root, text="Nombre").pack()
        self.nombre = tk.Entry(root); self.nombre.pack()

        tk.Label(root, text="Apellido").pack()
        self.apellido = tk.Entry(root); self.apellido.pack()

        tk.Label(root, text="Correo").pack()
        self.correo = tk.Entry(root); self.correo.pack()

        tk.Label(root, text="Fecha de matrícula (YYYY-MM-DD)").pack()
        self.fecha_matricula = tk.Entry(root); self.fecha_matricula.pack()

        tk.Button(root, text="Registrar", command=self.registrar).pack(pady=6)
        tk.Button(root, text="Ver estudiantes", command=self.ver_estudiantes).pack(pady=6)
        tk.Button(root, text="Aplicar cambios", command=self.confirmar_aplicar_cambios).pack(pady=6)

    def registrar(self):
        try:
            estudiante = registrar_estudiante(
                self.nombre.get(),
                self.apellido.get(),
                self.correo.get(),
                datetime.strptime(self.fecha_matricula.get(), "%Y-%m-%d").date()
            )
            messagebox.showinfo("Éxito", f"Estudiante {estudiante.nombre} registrado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")

    def ver_estudiantes(self):
        estudiantes = listar_estudiantes()
        lista = "\n".join([f"{e.id}: {e.nombre} {e.apellido} - {e.correo} - {e.fecha_matricula}" for e in estudiantes])
        messagebox.showinfo("Estudiantes registrados", lista if lista else "No hay registros aún.")

    def confirmar_aplicar_cambios(self):
        if messagebox.askyesno("Confirmar", "¿Deseas aplicar los cambios realizados? "):
            messagebox.showinfo("Aplicado", "Cambios aplicados correctamente.")
        else:
            messagebox.showinfo("Cancelado", "Los cambios no fueron aplicados.")

    def confirmar_cierre(self):
        if messagebox.askokcancel("Salir", "¿Seguro que deseas cerrar la ventana? "):
            self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = InterfazEstudiantes(root)
    root.mainloop()
