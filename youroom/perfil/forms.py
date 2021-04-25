from django import forms


class FotoPerfilForm(forms.Form):
    foto_perfil = forms.ImageField(widget=forms.FileInput(attrs={'id': 'cover_image', 'accept': '.jpg, .jpeg, .png'}), required=False)