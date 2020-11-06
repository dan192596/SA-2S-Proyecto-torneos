from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from Juegos.models import Juego
from .models import Torneo, Partida
from .serializers import TorneoSerializer, PartidaSerializer

from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

import requests
import random
import os
import jwt

# Create your views here.
class TorneoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not 'juego' in request.data or not 'usuarios' in request.data:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        cantidad_jugadores = len(request.data['usuarios'])
        jugadores_por_torneo = cantidad_jugadores
        while cantidad_jugadores > 1:
            cociente = cantidad_jugadores // 2
            residuo = cantidad_jugadores % 2
            if residuo != 0:
                return Response({"detail": "cantidad jugadores inaceptable"}, status=status.HTTP_400_BAD_REQUEST)
            if cociente == 1:
                break
            else:
                cantidad_jugadores = cociente
        cantidad_partidas_por_jugar = jugadores_por_torneo //2
        cantidad_partidas_jugadas = 0
        torneo = Torneo.objects.create(
                juego = Juego.objects.get(id=request.data['juego']), 
                cantidad_jugadores = jugadores_por_torneo,
                cantidad_partidas_por_jugar=cantidad_partidas_por_jugar,
                cantidad_partidas_jugadas=cantidad_partidas_jugadas
            )
        jugadores = request.data['usuarios']
        for i in range(cantidad_partidas_por_jugar):
            index_jugador = random.randrange(0,len(jugadores))
            jugador1 = jugadores.pop(index_jugador)
            index_jugador = random.randrange(0,len(jugadores))
            jugador2 = jugadores.pop(index_jugador)
            Partida.objects.create(jugador1=jugador1, jugador2=jugador2, torneo=torneo, orden=i)
        serializer = TorneoSerializer(torneo, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        torneo=Torneo.objects.get(id=id)
        Partida.objects.filter(torneo=torneo).delete()
        torneo.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self, request, id=None):
        if id==None:
            torneos = Torneo.objects.all()
            serializer = TorneoSerializer(torneos, many=True, context={'request': request})
            data = {
                'torneos': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        torneo = Torneo.objects.get(id=id)
        serializer = TorneoSerializer(torneo, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PartidaView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id=None):
        if id==None:
            partidas = Partida.objects.all()
            serializer = PartidaSerializer(partidas, many=True, context={'request': request})
            data = {
                'partidas': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        partida = Partida.objects.get(uuid=id)
        serializer = PartidaSerializer(partida, many=False, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        if os.environ['REVISAR_JWT'] =='True':
            try:
                authorizationHeader = request.META.get('HTTP_AUTHORIZATION')
                token = authorizationHeader.split()            
                f = open(os.environ['PUBLIC_JWT'], "r")
                public_key = f.read()
                jwt.unregister_algorithm('RS256')
                jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
                data = jwt.decode(token[1], public_key, audience='2' ,algorithm='RS256')
                valid = False            
                for scope in data['scopes']:
                    if scope == "torneos.partida.put":
                        valid = True
                if not valid:
                    print("Token invalido")
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                print("Token Valido")
            except:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        partida = Partida.objects.get(uuid =id)
        if len(request.data['marcador']) !=2:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        partida.jugador1_punteo = request.data['marcador'][0]
        partida.jugador2_punteo = request.data['marcador'][1]
        partida.completada = True
        partida.save()
        torneo = Torneo.objects.get(id=partida.torneo.id)
        torneo.cantidad_partidas_jugadas=torneo.cantidad_partidas_jugadas+1
        torneo.save()
        if torneo.cantidad_partidas_jugadas == torneo.cantidad_partidas_por_jugar and torneo.cantidad_partidas_por_jugar!=1:
            torneo.cantidad_partidas_jugadas = 0
            torneo.cantidad_partidas_por_jugar = torneo.cantidad_partidas_por_jugar /2
            torneo.cantidad_jugadores=torneo.cantidad_jugadores/2
            torneo.fase=torneo.fase+1
            torneo.save()
            partidas = Partida.objects.filter(torneo=torneo, fase=torneo.fase-1).order_by('orden')
            print(partidas)
            i = 0
            print(len(partidas))
            while i < len(partidas):
                print(i)
                jugador1 = partidas[i].jugador1 if partidas[i].jugador1_punteo > partidas[i].jugador2_punteo else partidas[i].jugador2
                i=i+1
                jugador2 = partidas[i].jugador1 if partidas[i].jugador1_punteo > partidas[i].jugador2_punteo else partidas[i].jugador2
                i=i+1
                Partida.objects.create(jugador1=jugador1, jugador2=jugador2, torneo=torneo, orden=i)
        return Response(status=status.HTTP_200_OK)