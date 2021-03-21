from django.shortcuts import render
from django.views.generic import TemplateView

class FormPubView(TemplateView):
    template_name = 'publicacion/publicacion.html'