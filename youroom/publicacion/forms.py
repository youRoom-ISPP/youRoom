from django import forms


class PublicacionForm(forms.Form):
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'id': 'imgInp', }))
