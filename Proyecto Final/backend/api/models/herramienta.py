from django.db import models
"""
la clase Herramienta representa una herramienta en el sistema de gestión de herramientas.
Contiene atributos clave como código, nombre, tipo, ubicación y estado.

Funciones clave:- 'codigo' es un identificador único para cada herramienta.
- 'estado' indica si la herramienta está disponible, prestada o en mantenimiento.
- Los campos 'created_at' y 'updated_at' rastrean la creación y última actualización de la herramienta.

"""
class Herramienta(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, default="General")  # antes: categoria
    ubicacion = models.CharField(max_length=100, null=True, blank=True)

    estado = models.CharField(
        max_length=20,
        choices=[
            ("disponible", "Disponible"),
            ("prestada", "Prestada"),
            ("en_mantenimiento", "En mantenimiento")
        ],
        default="disponible"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
