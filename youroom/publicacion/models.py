from django.db import models
from usuario.models import UsuarioPerfil


class Publicacion(models.Model):
    imagen = models.ImageField(upload_to='publicaciones/')
    descripcion = models.TextField(verbose_name='Descripcion', null=True)
    fecha_publicacion = models.DateTimeField(auto_now=True)
    categoria = models.CharField(max_length=250)
    usuario = models.ForeignKey(UsuarioPerfil, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        storage, path = self.imagen.storage, self.imagen.path
        super(Publicacion, self).delete(*args, **kwargs)
        storage.delete(path)


class Destacada(models.Model):
    es_destacada = models.BooleanField(verbose_name='Es destacada')
    fecha_destacada = models.DateTimeField(verbose_name='Fecha destacada')
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, primary_key=True)


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=10)
    enlace = models.TextField()
    coord_x = models.FloatField()
    coord_y = models.FloatField()
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.enlace
