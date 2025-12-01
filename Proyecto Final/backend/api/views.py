from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models.herramienta import Herramienta
from api.models.prestamo import Prestamo

from api.serializers.herramienta_serializer import HerramientaSerializer
from api.serializers.prestamo_serializer import PrestamoSerializer


# ============================================================
#                   HERRAMIENTAS
# ============================================================

class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Herramienta.objects.all()
    serializer_class = HerramientaSerializer
    lookup_field = "codigo"  

    def destroy(self, request, *args, **kwargs):

        codigo = kwargs.get("codigo")
        if not Herramienta.objects.filter(codigo=codigo).exists():
            return Response({"error": "Herramienta no encontrada"}, status=404)

        # También eliminar préstamos asociados?
        Prestamo.objects.filter(herramienta_codigo=codigo).delete()

        instance = Herramienta.objects.get(codigo=codigo)
        instance.delete()
        return Response(status=204)

    # Permitir actualizar incluso si no envían todos los campos
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


# ============================================================
#                          PRÉSTAMOS
# ============================================================

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

    def create(self, request, *args, **kwargs):

        codigo = request.data.get("herramienta_codigo")

        # Validar existencia
        try:
            herramienta = Herramienta.objects.get(codigo=codigo)
        except Herramienta.DoesNotExist:
            return Response({"detail": "Herramienta no existe."}, status=400)

        # Validar disponibilidad
        if herramienta.estado == "prestada":
            return Response({"detail": "Herramienta no disponible."}, status=400)

        # Crear préstamo
        response = super().create(request, *args, **kwargs)

        # Cambiar estado
        herramienta.estado = "prestada"
        herramienta.save()

        return response

    # DEVOLUCIÓN (update)
    def update(self, request, *args, **kwargs):

        instance = self.get_object()

        # Si viene fecha_devolucion → devolver herramienta
        if "fecha_devolucion" in request.data:

            codigo = instance.herramienta_codigo
            try:
                h = Herramienta.objects.get(codigo=codigo)
                h.estado = "disponible"
                h.save()
            except Herramienta.DoesNotExist:
                pass

        return super().update(request, *args, **kwargs)

    # Permitir eliminar un préstamo
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        # Si estaba activo, devolver herramienta
        if instance.estado == "activo":
            try:
                h = Herramienta.objects.get(codigo=instance.herramienta_codigo)
                h.estado = "disponible"
                h.save()
            except Herramienta.DoesNotExist:
                pass

        instance.delete()
        return Response(status=204)
