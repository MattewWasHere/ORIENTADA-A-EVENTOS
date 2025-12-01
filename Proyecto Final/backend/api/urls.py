from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import HerramientaViewSet, PrestamoViewSet

router = DefaultRouter()
router.register("herramientas", HerramientaViewSet, basename="herramienta")
router.register("prestamos", PrestamoViewSet, basename="prestamo")

urlpatterns = [
    path("", include(router.urls))
]
