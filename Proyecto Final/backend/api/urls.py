
from rest_framework import routers
from .views import HerramientaViewSet, PrestamoViewSet
router = routers.DefaultRouter()
router.register(r'herramientas', HerramientaViewSet, basename='herramienta')
router.register(r'prestamos', PrestamoViewSet, basename='prestamo')
urlpatterns = router.urls
