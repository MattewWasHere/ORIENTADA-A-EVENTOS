from rest_framework import serializers
from api.models.herramienta import Herramienta


class HerramientaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Herramienta
        fields = [
            "codigo",
            "nombre",
            "tipo",
            "ubicacion",
            "estado",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]
