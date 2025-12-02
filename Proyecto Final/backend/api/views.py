from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models.herramienta import Herramienta
from api.models.prestamo import Prestamo

from api.serializers.herramienta_serializer import HerramientaSerializer
from api.serializers.prestamo_serializer import PrestamoSerializer


class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Herramienta.objects.all()
    serializer_class = HerramientaSerializer
    lookup_field = "codigo"

    def destroy(self, request, *args, **kwargs):
        codigo = kwargs.get("codigo")
        if not Herramienta.objects.filter(codigo=codigo).exists():
            return Response({"error": "Herramienta no encontrada"}, status=404)
        # borrar prestamos relacionados (no hay FK)
        Prestamo.objects.filter(herramienta_codigo=codigo).delete()
        instance = Herramienta.objects.get(codigo=codigo)
        instance.delete()
        return Response(status=204)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

    def create(self, request, *args, **kwargs):
        codigo = request.data.get("herramienta_codigo")
        try:
            herramienta = Herramienta.objects.get(codigo=codigo)
        except Herramienta.DoesNotExist:
            return Response({"detail": "Herramienta no existe."}, status=400)

        if herramienta.estado == "prestada":
            return Response({"detail": "Herramienta no disponible."}, status=400)

        response = super().create(request, *args, **kwargs)
        herramienta.estado = "prestada"
        herramienta.save()
        return response

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if "fecha_devolucion" in request.data and request.data.get("fecha_devolucion"):
            codigo = instance.herramienta_codigo
            try:
                h = Herramienta.objects.get(codigo=codigo)
                h.estado = "disponible"
                h.save()
            except Herramienta.DoesNotExist:
                pass
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.estado == "activo" or instance.estado == "prestado" or instance.estado == "activo":
            try:
                h = Herramienta.objects.get(codigo=instance.herramienta_codigo)
                h.estado = "disponible"
                h.save()
            except Herramienta.DoesNotExist:
                pass
        instance.delete()
        return Response(status=204)
