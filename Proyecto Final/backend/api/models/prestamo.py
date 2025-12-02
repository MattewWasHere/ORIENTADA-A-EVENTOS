from django.db import models
"""
la clase Prestamo representa un registro de préstamo de una herramienta en el sistema.
Contiene información sobre la herramienta prestada, las personas involucradas,

Fucniones clave:  'herramienta_codigo' vincula el préstamo a una herramienta específica mediante su código.
'responsable' indica quién es responsable del préstamo.

"""
class Prestamo(models.Model):
    herramienta_codigo = models.CharField(max_length=50)
    responsable = models.CharField(max_length=200)
    persona_entrega = models.CharField(max_length=200, blank=True)
    persona_recibe = models.CharField(max_length=200, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    fecha_prevista = models.DateField(null=True, blank=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=30, default="activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "api_prestamo"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Prestamo {self.id} - {self.herramienta_codigo}"
