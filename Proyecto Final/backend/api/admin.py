from django.contrib import admin
from api.models.herramienta import Herramienta
from api.models.prestamo import Prestamo


@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "tipo", "ubicacion", "estado", "created_at")
    search_fields = ("codigo", "nombre", "tipo")
    list_filter = ("estado", "tipo")


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "herramienta_codigo",
        "responsable",
        "fecha_entrega",     
        "fecha_prevista",
        "fecha_devolucion",
        "estado",
    )

    search_fields = ("herramienta_codigo", "responsable")
    list_filter = ("estado",)
