from django import forms
from publicacion.enum import Categorias


class PublicacionForm(forms.Form):
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'id': 'imgInp', }))
    descripcion = forms.CharField(label='Descripción de la publicación', required=True)
    categoria = forms.ChoiceField(label='Categoria de la foto', choices=Categorias.choices(), required=True)
