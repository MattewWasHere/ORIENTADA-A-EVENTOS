from django.contrib import admin
from .models import Estudiante

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'edad', 'correo_electronico', 'fecha_matricula')
