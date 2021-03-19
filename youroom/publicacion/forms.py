from django import forms
from publicacion.models import Publicacion
from publicacion.enum import Categorias

class FormularioPublicacion(forms.Form):
    descripcion = forms.CharField(label='Descripción de la publicación', required=True)
    categoria = forms.ChoiceField(label='Categoria de la foto', choices=Categorias.choices(), required=True)
