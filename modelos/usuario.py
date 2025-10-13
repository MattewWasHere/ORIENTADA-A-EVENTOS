import tkinter as tk

class Estudiante():
    def __init__(self,RegistroEstudiante):
        self.RegistroEstudiante = RegistroEstudiante
        self.nombre = tk.StringVar(RegistroEstudiante)
        self.edad = tk.IntVar(RegistroEstudiante)
        self.correo = tk.StringVar(RegistroEstudiante)
        self.fecha_matricula = tk.StringVar(RegistroEstudiante) 
        