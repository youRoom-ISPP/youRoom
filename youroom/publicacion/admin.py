from django.contrib import admin
from .models import Publicacion, Etiqueta, Destacada

admin.site.register(Publicacion)
admin.site.register(Etiqueta)
admin.site.register(Destacada)
