from django.shortcuts import render
from django.views.generic import TemplateView
from publicacion.models import Publicacion
from ranking.forms import ValoracionForm


class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publicaciones'] = Publicacion.objects.all()
        context['formulario_valoracion'] = ValoracionForm()
        return context
