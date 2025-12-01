
from rest_framework import serializers
from api.models.herramienta import Herramienta
class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramienta
        fields = ['id','codigo','nombre','descripcion','cantidad','ubicacion','estado','created_at']
        read_only_fields = ['id','created_at']
