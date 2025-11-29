from django.contrib import admin
from .models import Herramienta, Prestamo
@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre','tipo','estado')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('consecutivo','herramienta_codigo','usuario','fecha_salida')
