from django import forms


class PerfilForm(forms.Form):
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'id': 'imagen', }), required=True)
    descripcion = forms.CharField(label='',widget=forms.Textarea(attrs={'id': 'descripcion-reg', 'class': 'form-control', 'placeholder': 'Descríbete en pocas palabras', 'rows': '3'}),max_length=280,required=False)
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id': 'password-reg', 'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id': 'password-confirm-reg', 'class': 'form-control', 'placeholder': 'Repite la contraseña'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
                msg = 'Las contraseñas deben de coincidir.'
                self._errors['password1'] = self.error_class([msg])
                del self.cleaned_data['password1']
                del self.cleaned_data['password2']
        return self.cleaned_data
