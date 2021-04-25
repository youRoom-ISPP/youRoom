from django import forms


class EditarPerfilForm(forms.Form):
    descripcion = forms.CharField(label='', widget=forms.Textarea(attrs={'id': 'descripcion-reg', 'class': 'form-control my-3', 'placeholder': 'Descríbete en pocas palabras', 'rows': '3'}), max_length=280, required=False)
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'id': 'password-reg', 'class': 'form-control mb-3', 'placeholder': 'Nueva contraseña'}), required=False, min_length=8)
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'id': 'password-confirm-reg', 'class': 'form-control mb-3', 'placeholder': 'Repite la contraseña'}), required=False, min_length=8)
