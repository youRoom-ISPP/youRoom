from django.shortcuts import render
from django.views.generic import TemplateView
from publicacion.models import Publicacion, Destacada
from publicacion.enum import Categorias
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class TimelineViewCategorias(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        categoria = Categorias.choices()[int(pk)][0]
        context['publicaciones'] = Publicacion.objects.filter(categoria=categoria)
        context['categorias'] = Categorias.choices()
        return context

@method_decorator(login_required, name='dispatch')
class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        res = Destacada.objects.all()
        publicaciones = []
        for destacada in res:
            publicaciones.append(destacada.publicacion)
        context['publicaciones'] = publicaciones
        context['categorias'] = Categorias.choices()
        return context


