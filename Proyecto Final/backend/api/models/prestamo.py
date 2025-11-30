from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from api.models.herramienta import Herramienta

def generar_consecutivo_por_tiempo():
    now = timezone.now()
    return f"P-{now.strftime('%Y%m%d-%H%M%S')}"

class Prestamo(models.Model):
    consecutivo = models.CharField(max_length=50, unique=True, blank=True)
    herramienta_codigo = models.CharField(max_length=50)
    usuario = models.CharField(max_length=200)
    fecha_salida = models.DateTimeField()
    fecha_prevista = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not Herramienta.objects.filter(codigo=self.herramienta_codigo).exists():
            raise ValidationError({"herramienta_codigo": f"Herramienta con código '{self.herramienta_codigo}' no existe."})
        super().clean()

    def save(self, *args, **kwargs):
        if not self.consecutivo:
            candidato = generar_consecutivo_por_tiempo()
            suffix = 0
            base = candidato
            while Prestamo.objects.filter(consecutivo=candidato).exists():
                suffix += 1
                candidato = f"{base}-{suffix}"
            self.consecutivo = candidato
        self.full_clean()
        try:
            h = Herramienta.objects.get(codigo=self.herramienta_codigo)
            h.estado = 'prestado'
            h.save(update_fields=['estado'])
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.consecutivo} -> {self.herramienta_codigo}"
