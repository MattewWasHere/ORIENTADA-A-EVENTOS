
from django.db import models
from django.utils import timezone
class Prestamo(models.Model):
    herramienta_codigo = models.CharField(max_length=50)
    persona_entrega = models.CharField(max_length=200, blank=True)
    persona_recibe = models.CharField(max_length=200)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    fecha_prevista = models.DateTimeField(null=True, blank=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=30, default='activo')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return f"Prestamo {self.id} - {self.herramienta_codigo}"
