from rest_framework import serializers
from api.models.prestamo import Prestamo


class PrestamoSerializer(serializers.ModelSerializer):
    fecha_entrega = serializers.DateTimeField(required=False, allow_null=True)
    fecha_prevista = serializers.DateTimeField(required=False, allow_null=True)
    fecha_devolucion = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Prestamo
        fields = [
            'id',
            'herramienta_codigo',
            'persona_entrega',
            'persona_recibe',
            'fecha_entrega',
            'fecha_prevista',
            'fecha_devolucion',
            'estado',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Si se registra fecha_devolución → cerrar préstamo automáticamente
        if 'fecha_devolucion' in validated_data and validated_data['fecha_devolucion'] is not None:
            instance.estado = 'cerrado'

        instance.save()
        return instance
