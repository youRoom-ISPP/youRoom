from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver


class UsuarioPerfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    descripcion = models.TextField(max_length=500, blank=True)
    totalPuntos = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    id_stripe = models.CharField(max_length=50, blank=True, default='')
    foto_perfil = models.ImageField(upload_to='perfil/', default='')

class ContadorVida(models.Model):
    perfil = models.OneToOneField(UsuarioPerfil, on_delete=models.CASCADE,)
    numVidasSemanales = models.IntegerField(default=3,validators=[MinValueValidator(0), MaxValueValidator(3)])
    numVidasCompradas = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    estaActivo = models.BooleanField(default=True)

    def clean(self):
        if self.estaActivo == True and Premium.objects.filter(perfil_id=self.perfil.id).exists() == True:
            raise ValidationError(('El usuario es premium, con lo que no puede tener activado el contador.'))


class Premium(models.Model):
    perfil = models.OneToOneField(UsuarioPerfil, on_delete=models.CASCADE, null=True, blank=True)
    fechaSuscripcion = models.DateField(auto_now_add=True)
    fechaCancelacion = models.DateField(null=True,blank = True)

    def clean(self):
        if self.perfil.contadorvida.estaActivo == True:
            ContadorVida.objects.filter(perfil_id=self.perfil.id).update(estaActivo=False)


@receiver(models.signals.post_delete, sender=Premium)
def activar_contador(sender, instance, *args, **kwargs):
    ContadorVida.objects.filter(perfil_id=instance.perfil.id).update(estaActivo=True)
