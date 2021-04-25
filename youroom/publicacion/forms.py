from django import forms
from .enum import Categorias


class PublicacionForm(forms.Form):
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'id': 'imagen', }), required=True)
    categoria = forms.ChoiceField(widget=forms.Select(attrs={'id': 'categoria', 'class': 'form-control'}), label='Categoria', choices=Categorias.choices(), required=True)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'id': 'descripcion', 'class': 'form-control', 'placeholder': 'Describe tu imagen...', 'rows': '3'}), required=False)
    etiquetas = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'etiquetas'}), required=False)

class ComentarioForm(forms.Form):
    texto = forms.CharField(required=True)
    publicacion_id = forms.IntegerField(widget=forms.HiddenInput(),required=True)
