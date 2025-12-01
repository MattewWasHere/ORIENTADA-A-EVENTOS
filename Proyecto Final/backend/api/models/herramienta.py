
from django.db import models
class Herramienta(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    cantidad = models.IntegerField(default=1)
    ubicacion = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=30, default='disponible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
