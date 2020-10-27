from django.db import models

# Create your models here.
class Juego(models.Model):
    nombre = models.TextField(editable=True)
    ip = models.TextField(editable=True)    
    
    def __str__(self):
        return self.nombre