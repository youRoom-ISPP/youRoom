from django.db import models
from usuario.models import UsuarioPerfil


class Publicacion(models.Model):
    imagen = models.ImageField(upload_to='publicaciones/')
    descripcion = models.TextField(verbose_name='Descripcion', null=True)
    fecha_publicacion = models.DateTimeField(auto_now=True)
    categoria = models.CharField(max_length=250, null=True)
    usuario = models.ForeignKey(UsuarioPerfil, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.descripcion


class Destacada(models.Model):
    es_destacada = models.BooleanField(verbose_name='Es destacada')
    fecha_destacada = models.DateTimeField(verbose_name='Fecha destacada')
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, primary_key=True)
