from django.shortcuts import render
from django.views.generic import TemplateView
from publicacion.models import Publicacion, Destacada
from publicacion.enum import Categorias


class TimelineViewCategorias(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['publicaciones'] = Publicacion.objects.filter(categoria=pk)
        return context

class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        res = Destacada.objects.all()
        publicaciones = []
        for destacada in res:
            publicaciones.append(destacada.publicacion)
        context['publicaciones'] = publicaciones
        return context