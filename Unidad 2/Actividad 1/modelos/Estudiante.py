import tkinter as tk
from datetime import date

class Estudiante():
    def __init__(self, root):
        self.root = root
        self.nombre = tk.StringVar(root)
        self.apellido = tk.StringVar(root)
        self.correo = tk.StringVar(root)
        self.fecha_matricula = tk.StringVar(root)
    
    def obtener_datos(self):
        return {
            'nombre': self.nombre.get(),
            'apellido': self.apellido.get(),
            'correo': self.correo.get(),
            'fecha_matricula': self.fecha_matricula.get()
        }
    
    def limpiar_campos(self):
        self.nombre.set('')
        self.apellido.set('')
        self.correo.set('')
        self.fecha_matricula.set('')

class Cargue():
    def __init__(self, root):
        self.root = root
        self.placa_vehiculo = tk.StringVar(root)
        self.valor_cargue = tk.IntVar(root)
        self.tipo_carga = tk.StringVar(root)
        self.vencimiento_soat = tk.StringVar(root)