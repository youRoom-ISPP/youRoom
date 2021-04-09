from django import forms
from django.contrib.auth.models import User


class RegistroForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=254)
    descripcion = forms.CharField(widget=forms.Textarea(),max_length=280,required=False)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        if password1 != password2:
                msg = 'Las contraseñas deben de coincidir.'
                self._errors['password1'] = self.error_class([msg])
                del self.cleaned_data['password1']
                del self.cleaned_data['password2']
        if User.objects.filter(username=username).exists():
                msg = 'El nombre de usuario no está disponible.'
                self._errors['username'] = self.error_class([msg])
                del self.cleaned_data['username']
        if User.objects.filter(email=email).exists():
                msg = 'El e-mail introducido ya se encuentra registrado.'
                self._errors['email'] = self.error_class([msg])
                del self.cleaned_data['email']
        return self.cleaned_data
