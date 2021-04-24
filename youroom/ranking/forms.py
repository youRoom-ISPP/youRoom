from django import forms


class ValoracionForm(forms.Form):
    puntuacion = forms.ChoiceField(label='Valoración', choices=((1, '1'), (2, '2'), (3, '3'),
                                                                (4, '4'), (5, '5')), required=True)
    publicacion_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)