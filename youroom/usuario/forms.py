from django import forms


class RegistroForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=254)
    descripcion = forms.CharField(widget=forms.Textarea(),max_length=280,required=False)