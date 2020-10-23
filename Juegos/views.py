from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Juego
from .serializers import JuegoSerializer

import requests
import random
import os

# Create your views here.
class JuegoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not 'ip' in request.data or not 'name' in request.data:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        juego = Juego.objects.create(ip=request.data['ip'], nombre=request.data['nombre'])
        response = {
            "id":juego.id,
            "nombres":juego.nombre,
            "apellidos":juego.ip
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, id=None):
        if id==None:
            juegos = Juego.objects.all()
            serializer = JuegoSerializer(juegos, many=True, context={'request': request})
            data = {
                'juegos': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        juego = Juego.objects.get(id=id)
        response = {
            "id":juego.id,
            "nombres":juego.nombre,
            "apellidos":juego.ip
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, id):
        juego = Juego.objects.get(id=id)
        juego.ip = request.data['ip']
        juego.nombre = request.data['nombre']
        juego.save()
        response = {
            "id":juego.id,
            "nombres":juego.nombre,
            "apellidos":juego.ip
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        Juego.objects.get(id=id).delete()
        return Response(status=status.HTTP_200_OK)

