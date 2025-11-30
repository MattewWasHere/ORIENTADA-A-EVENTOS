from rest_framework import viewsets
from api.models import Herramienta, Prestamo
from api.serializers.herramienta_serializer import HerramientaSerializer
from api.serializers.prestamo_serializer import PrestamoSerializer

class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Herramienta.objects.all().order_by('codigo')
    serializer_class = HerramientaSerializer
    lookup_field = 'codigo'


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all().order_by('consecutivo')
    serializer_class = PrestamoSerializer
    lookup_field = 'consecutivo'
