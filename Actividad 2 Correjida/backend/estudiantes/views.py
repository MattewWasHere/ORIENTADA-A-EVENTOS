from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Estudiante
from .serializers import EstudianteSerializer

class EstudianteListCreate(APIView):
    def get(self, request, format=None):
        estudiantes = Estudiante.objects.all()
        serializer = EstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EstudianteDetail(APIView):
    def get_object(self, pk):
        try:
            return Estudiante.objects.get(pk=pk)
        except Estudiante.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        estudiante = self.get_object(pk)
        serializer = EstudianteSerializer(estudiante)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        estudiante = self.get_object(pk)
        serializer = EstudianteSerializer(estudiante, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        estudiante = self.get_object(pk)
        estudiante.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
