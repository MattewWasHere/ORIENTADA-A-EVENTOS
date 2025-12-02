from rest_framework import serializers
from api.models.prestamo import Prestamo


class PrestamoSerializer(serializers.ModelSerializer):
    """
    Serializador del modelo Prestamo.

    Este serializador controla:
    - Validación dinámica para creación y actualización.
    - Campos de fecha opcionales y convertidos a formato estándar.
    - Eliminación del error al devolver préstamos (PATCH sin requerir 'responsable').
    """

    # ------------------------------------------------------------
    #   CAMPOS DEFINIDOS MANUALMENTE PARA CONTROL FINO
    # ------------------------------------------------------------
    # Todos estos campos son opcionales, porque un PATCH (devolución)
    # NO debe exigirlos.
    fecha_entrega = serializers.DateField(required=False, allow_null=True)
    fecha_prevista = serializers.DateField(required=False, allow_null=True)
    fecha_devolucion = serializers.DateField(required=False, allow_null=True)

    # ------------------------------------------------------------
    #   CONFIGURACIÓN PRINCIPAL DEL SERIALIZER
    # ------------------------------------------------------------
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

        # Campos que NO deben modificarse nunca desde el frontend
        read_only_fields = ["id", "created_at", "updated_at"]

        # Marcamos todos como opcionales (para PATCH)
        extra_kwargs = {
            "responsable": {"required": False},
            "persona_entrega": {"required": False},
            "persona_recibe": {"required": False},
            "fecha_entrega": {"required": False},
            "fecha_prevista": {"required": False},
            "estado": {"required": False},
        }

    # ------------------------------------------------------------
    #   VALIDACIÓN PERSONALIZADA
    # ------------------------------------------------------------
    def validate(self, data):
        """
        Reglas de validación:

        ✔ Si es POST (crear préstamo)
          → 'responsable' ES obligatorio.

        ✔ Si es PATCH (devolver préstamo)
          → NO exigir responsable ni otros campos.

        Esto elimina completamente el error:
        {"responsable": ["Este campo es requerido."]}
        al devolver un préstamo.
        """

        request = self.context.get("request")

        # Validación solamente en creación
        if request and request.method == "POST":
            if not data.get("responsable"):
                raise serializers.ValidationError({
                    "responsable": "Este campo es requerido al crear un préstamo."
                })

        return data
