
from rest_framework.viewsets import ModelViewSet
from .models.herramienta import Herramienta
from .models.prestamo import Prestamo
from .serializers import HerramientaSerializer, PrestamoSerializer

class HerramientaViewSet(ModelViewSet):
    queryset = Herramienta.objects.all().order_by('id')
    serializer_class = HerramientaSerializer
    lookup_field = 'codigo'

class PrestamoViewSet(ModelViewSet):
    queryset = Prestamo.objects.all().order_by('id')
    serializer_class = PrestamoSerializer
