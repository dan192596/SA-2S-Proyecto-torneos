from django.db import models

from Juegos.models import Juego

import uuid
# Create your models here.

class Torneo(models.Model):
    juego = models.ForeignKey(Juego, on_delete=True, related_name='User')
    cantidad_jugadores = models.IntegerField(default=0)
    cantidad_partidas_por_jugar = models.IntegerField(default=0)
    cantidad_partidas_jugadas = models.IntegerField(default=0)
    
    def __str__(self):
        return self.id

class Partida(models.Model):
    jugador1 = models.CharField(blank=False, null=False, max_length=10)
    jugador1_punteo = models.IntegerField(default=0)
    jugador2 = models.CharField(blank=False, null=False, max_length=10)
    jugador2_punteo = models.IntegerField(default=0)
    uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    completada = models.BooleanField(default=False)
    torneo = models.ForeignKey(Torneo, on_delete=True, related_name='torneo')

    def __str__(self):
        return self.id