from .models import Juego
from rest_framework import serializers

#Serializador para retornar la lista de todas las clases existentes
class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juego
        fields = ('id', 'nombre', 'ip')