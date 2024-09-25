from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Notas(models.Model):
    titulo = models.CharField(max_length=25)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo