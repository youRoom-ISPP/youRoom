from django import forms
from django.contrib.auth.models import User


class RegistroForm(forms.Form):
    username = forms.CharField(label='',widget=forms.TextInput(attrs={'id': 'username-reg', 'class': 'form-control','placeholder': 'Nombre de usuario'}),max_length=30)
    email = forms.EmailField(label='',max_length=254, widget=forms.TextInput(attrs={'id': 'email-reg', 'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id': 'password-reg', 'class': 'form-control', 'placeholder': 'Contraseña'}), min_length=8)
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id': 'password-confirm-reg', 'class': 'form-control', 'placeholder': 'Repite la contraseña'}), min_length=8)
    descripcion = forms.CharField(label='',widget=forms.Textarea(attrs={'id': 'descripcion-reg', 'class': 'form-control', 'placeholder': 'Descríbete en pocas palabras', 'rows': '3'}),max_length=280,required=False)

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
