from django.contrib import admin

# Register your models here.
from .models import UsuarioPerfil, Premium, ContadorVida

admin.site.register(UsuarioPerfil)
admin.site.register(Premium)
admin.site.register(ContadorVida)
