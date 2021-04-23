from django import forms


class PerfilForm(forms.Form):
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'id': 'imagen', }), required=False)
    descripcion = forms.CharField(label='',widget=forms.Textarea(attrs={'id': 'descripcion-reg', 'class': 'form-control', 'placeholder': 'Descríbete en pocas palabras', 'rows': '3'}),max_length=280,required=False)
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id': 'password-reg', 'class': 'form-control', 'placeholder': 'Contraseña'}),required=False, min_length=8)
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={'id': 'password-confirm-reg', 'class': 'form-control', 'placeholder': 'Repite la contraseña'}),required=False,min_length=8)

