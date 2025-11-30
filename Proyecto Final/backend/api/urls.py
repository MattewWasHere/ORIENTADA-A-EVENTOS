from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import HerramientaViewSet, PrestamoViewSet

router = DefaultRouter()
router.register(r'herramientas', HerramientaViewSet, basename='herramienta')
router.register(r'prestamos', PrestamoViewSet, basename='prestamo')

urlpatterns = [
    path('', include(router.urls)),
]
