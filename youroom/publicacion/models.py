import os
import boto3
from django.db import models
from usuario.models import UsuarioPerfil
from django.core.validators import MinValueValidator
from dotenv import load_dotenv

load_dotenv()
BUCKET_NAME = os.environ.get("S3_BUCKET")
s3 = boto3.client('s3')


class Publicacion(models.Model):
    imagen = models.ImageField(upload_to='publicaciones/')
    descripcion = models.TextField(verbose_name='Descripcion', null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=250)
    usuario = models.ForeignKey(UsuarioPerfil, on_delete=models.CASCADE)
    totalValoraciones = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])

    def delete(self, *args, **kwargs):
        if os.getenv('PROD') == 'True':
            s3.delete_object(Bucket=BUCKET_NAME, Key=str(self.imagen.name))
            super(Publicacion, self).delete(*args, **kwargs)
        else:
            storage, path = self.imagen.storage, self.imagen.path
            super(Publicacion, self).delete(*args, **kwargs)
            storage.delete(path)


class Destacada(models.Model):
    es_destacada = models.BooleanField(verbose_name='Es destacada')
    fecha_destacada = models.DateTimeField(auto_now_add=True, verbose_name='Fecha destacada')
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, primary_key=True)


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=10)
    enlace = models.TextField()
    coord_x = models.FloatField()
    coord_y = models.FloatField()
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.enlace

class Comentario(models.Model):
    texto = models.TextField()
    usuario = models.ForeignKey(UsuarioPerfil, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)