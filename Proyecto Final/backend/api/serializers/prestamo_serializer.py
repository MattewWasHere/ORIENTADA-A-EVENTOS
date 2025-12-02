from rest_framework import serializers
from api.models.prestamo import Prestamo


class PrestamoSerializer(serializers.ModelSerializer):
    fecha_entrega = serializers.DateField(required=False, allow_null=True)
    fecha_prevista = serializers.DateField(required=False, allow_null=True)
    fecha_devolucion = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Prestamo
        fields = [
            "id",
            "herramienta_codigo",
            "responsable",
            "persona_entrega",
            "persona_recibe",
            "fecha_entrega",
            "fecha_prevista",
            "fecha_devolucion",
            "estado",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

        extra_kwargs = {
            "responsable": {"required": False},
            "persona_entrega": {"required": False},
            "persona_recibe": {"required": False},
            "fecha_entrega": {"required": False},
            "fecha_prevista": {"required": False},
            "estado": {"required": False},
        }

    def validate(self, data):
        request = self.context.get("request")

        # Solo exigir "responsable" en creación
        if request and request.method == "POST":
            if not data.get("responsable"):
                raise serializers.ValidationError({
                    "responsable": "Este campo es requerido."
                })

        return data
