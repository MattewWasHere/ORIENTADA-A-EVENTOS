from django.db import models

class Herramienta(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=50) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Prestamo(models.Model):
    consecutivo = models.CharField(max_length=50, unique=True)
    herramienta_codigo = models.CharField(max_length=50)  
    usuario = models.CharField(max_length=200)
    fecha_salida = models.DateTimeField()
    fecha_prevista = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.consecutivo} -> {self.herramienta_codigo}"
