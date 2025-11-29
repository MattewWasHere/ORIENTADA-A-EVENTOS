from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Herramienta, Prestamo
from .serializers import HerramientaSerializer, PrestamoSerializer
from django.db import transaction

class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Herramienta.objects.all().order_by('codigo')
    serializer_class = HerramientaSerializer
    lookup_field = 'codigo'


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all().order_by('consecutivo')
    serializer_class = PrestamoSerializer
    lookup_field = 'consecutivo'

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        codigo = data.get('herramienta_codigo')
        if not codigo:
            return Response({'error': 'herramienta_codigo es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # intentar reservar la herramienta de forma segura
            with transaction.atomic():
                herramienta = Herramienta.objects.select_for_update().get(codigo=codigo)
                if herramienta.estado.lower() != 'disponible':
                    return Response({'error': 'La herramienta no está disponible'}, status=status.HTTP_400_BAD_REQUEST)
                # cambiar estado a prestada
                herramienta.estado = 'prestada'
                herramienta.save()
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Herramienta.DoesNotExist:
            return Response({'error': 'Herramienta no encontrada'}, status=status.HTTP_400_BAD_REQUEST)
