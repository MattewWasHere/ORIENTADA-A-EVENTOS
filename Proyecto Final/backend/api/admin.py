
from django.contrib import admin
from .models.herramienta import Herramienta
from .models.prestamo import Prestamo
admin.site.register(Herramienta)
admin.site.register(Prestamo)
