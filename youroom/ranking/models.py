from django.db import models
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil
from django.core.validators import MaxValueValidator, MinValueValidator


class Valoracion(models.Model):
    usuario = models.ForeignKey(UsuarioPerfil, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])