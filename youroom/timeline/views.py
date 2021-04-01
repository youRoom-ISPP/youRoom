from django.shortcuts import render
from django.views.generic import TemplateView
from publicacion.models import Publicacion, Destacada
from ranking.forms import ValoracionForm
from publicacion.enum import Categorias
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone


@method_decorator(login_required, name='dispatch')
class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        publicaciones = []
        for destacada in Destacada.objects.all():
            if (datetime.now(timezone.utc) - destacada.fecha_destacada).total_seconds()>86400:
                destacada.delete()
            else:
                publicaciones.append(destacada.publicacion)


        publicaciones.sort(key=lambda x: x.fecha_publicacion, reverse=True)

        for publicacion in Publicacion.objects.all().order_by('-fecha_publicacion'):
            if publicacion not in publicaciones:
                publicaciones.append(publicacion)
        context['formulario_valoracion'] = ValoracionForm()
        context['publicaciones'] = publicaciones
        context['categorias'] = Categorias.choices()
        return context

@method_decorator(login_required, name='dispatch')
class TimelineViewCategorias(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria_seleccionada = self.kwargs.get('categoria')

        categoria=None
        for tupla in Categorias.choices():
            if tupla[1] == categoria_seleccionada:
                categoria = tupla[0]
                break

        context['publicaciones'] = Publicacion.objects.filter(categoria=categoria).order_by('-fecha_publicacion')
        context['categorias'] = Categorias.choices()
        return context