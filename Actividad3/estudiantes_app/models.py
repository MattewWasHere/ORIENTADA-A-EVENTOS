from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    correo_electronico = models.EmailField(unique=True)
    fecha_matricula = models.DateField()

    def __str__(self):
        return self.nombre
