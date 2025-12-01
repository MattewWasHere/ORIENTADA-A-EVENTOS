from rest_framework import serializers
from api.models.prestamo import Prestamo


class PrestamoSerializer(serializers.ModelSerializer):
    # Campos de fecha opcionales
    fecha_salida = serializers.DateField(required=False, allow_null=True)
    fecha_prevista = serializers.DateField(required=False, allow_null=True)
    fecha_entrega = serializers.DateField(required=False, allow_null=True)
    fecha_devolucion = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Prestamo
        fields = [
            "id",
            "herramienta_codigo",
            "responsable",
            "persona_entrega",
            "persona_recibe",
            "fecha_salida",
            "fecha_prevista",
            "fecha_entrega",
            "fecha_devolucion",
            "estado",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    # Limpieza de código herramienta
    def validate_herramienta_codigo(self, value):
        return str(value).strip()

    # VALIDACIÓN GLOBAL REPARADA
    def validate(self, data):

        # Si no envían responsable -> usar persona_entrega
        if not data.get("responsable"):
            data["responsable"] = data.get("persona_entrega", "N/A")

        return data

    # CREATE REPARADO
    def create(self, validated_data):

        # Autocompletar responsable si viene vacío
        if not validated_data.get("responsable"):
            validated_data["responsable"] = validated_data.get("persona_entrega", "N/A")

        return super().create(validated_data)

    # UPDATE REPARADO (para devoluciones)
    def update(self, instance, validated_data):

        # Para update nunca forzar "responsable"
        if not validated_data.get("responsable"):
            validated_data["responsable"] = instance.responsable

        return super().update(instance, validated_data)
