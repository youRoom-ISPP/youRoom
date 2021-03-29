from usuario.models import ContadorVida
def restablecerVidas():
    for cont in ContadorVida.objects.all():
        cont.numVidasSemanales=3
        cont.save()