from .models import Torneo, Partida
from rest_framework import serializers



class PartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = ('id', 'jugador1', 'jugador1_punteo', 'jugador2', 'jugador2_punteo', 'uuid', 'completada', 'torneo')

#Serializador para retornar la lista de todas las clases existentes
class TorneoSerializer(serializers.ModelSerializer):
    partidas = serializers.SerializerMethodField('get_partidas')
    class Meta:
        model = Torneo
        fields = ('id', 'juego', 'cantidad_jugadores', 'cantidad_partidas_por_jugar', 'cantidad_partidas_jugadas', 'partidas')
    
    def get_partidas(self, obj):
        partidas = Partida.objects.filter(torneo=obj)
        serializer = PartidaSerializer(partidas, many=True)
        return serializer.data