from django.contrib import admin
from api.models import Herramienta, Prestamo

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo','nombre','categoria','estado','ubicacion')
    search_fields = ('codigo','nombre','categoria')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('consecutivo','herramienta_codigo','usuario','fecha_salida','fecha_devolucion')
    search_fields = ('consecutivo','herramienta_codigo','usuario')
