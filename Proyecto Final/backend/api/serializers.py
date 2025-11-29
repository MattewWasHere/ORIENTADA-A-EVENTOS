from rest_framework import serializers
from .models import Herramienta, Prestamo
from datetime import datetime


class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramienta
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        # OCULTAMOS consecutivo para el frontend
        fields = [
            'herramienta_codigo',
            'usuario',
            'fecha_salida',
            'fecha_prevista',
            'fecha_devolucion'
        ]
        read_only_fields = ('created_at', 'updated_at')
