from django.urls import path
from .views import EstudianteListCreate, EstudianteDetail

urlpatterns = [
    path('estudiantes/', EstudianteListCreate.as_view(), name='estudiantes-list'),
    path('estudiantes/<int:pk>/', EstudianteDetail.as_view(), name='estudiante-detail'),
]
