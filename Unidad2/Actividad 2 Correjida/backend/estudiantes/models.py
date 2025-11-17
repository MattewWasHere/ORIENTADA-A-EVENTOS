from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    fecha_matricula = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
