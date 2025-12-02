from rest_framework import serializers
from api.models.herramienta import Herramienta


class HerramientaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Herramienta.

    Este serializador transforma los datos del modelo en JSON para la API
    y valida las entradas que provienen del frontend.

    Funcionalidades clave:
    --------------------------------------------------------
    - Controla qué campos pueden crearse o actualizarse.
    - Garantiza que 'codigo' sea manejado correctamente como identificador.
    - Protege los campos automáticos:
        • id
        • created_at
        • updated_at
    - Facilita operaciones CRUD desde el frontend sin llaves foráneas.
    """

    class Meta:
        model = Herramienta

        # Campos expuestos por la API
        fields = [
            "id",
            "codigo",
            "nombre",
            "tipo",
            "ubicacion",
            "estado",
            "created_at",
            "updated_at",
        ]

        # Campos que NO pueden ser modificados directamente
        read_only_fields = ["id", "created_at", "updated_at"]

        """
        Notas importantes:
        ------------------
        ✔ 'codigo' funciona como identificador primario para el ViewSet
          (lookup_field = "codigo").

        ✔ 'estado' puede ser:
              - "disponible"
              - "prestada"
           y lo maneja el backend automáticamente cuando se crean o
           devuelven préstamos.

        ✔ El serializer permite que la herramienta se actualice sin
          requerir enviar todos los campos (PATCH compatible).
        """
