from django.db import models
from publicacion.enum import Categorias

#   Modelo de publicacion
class Publicacion(models.Model):
    descripcion =  models.TextField(verbose_name='Descripcion', null = True)
    fecha_publicacion = models.DateTimeField(verbose_name ='Fecha publicacion')
    categoria = models.CharField(default=Categorias.DORMITORIO, choices=Categorias.choices(), max_length=255)

    def __str__(self):
        return self.descripcion


class Destacada(models.Model):
    es_destacada  = models.BooleanField(verbose_name='Es destacada')
    fecha_destacada = models.DateTimeField(verbose_name= 'Fecha destacada')
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE,primary_key=True)

