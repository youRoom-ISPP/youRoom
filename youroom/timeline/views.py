from django.shortcuts import render
from django.views.generic import TemplateView
from publicacion.models import Publicacion, Destacada
from ranking.forms import ValoracionForm
from ranking.models import Valoracion
from usuario.models import UsuarioPerfil
from publicacion.enum import Categorias
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class TimelineView(TemplateView):
    template_name = 'timeline/timeline.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        publicaciones = []
        for destacada in Destacada.objects.all():
            publicaciones.append(destacada.publicacion)

        publicaciones.sort(key=lambda x: x.fecha_publicacion, reverse=True)

        for publicacion in Publicacion.objects.all().order_by('-fecha_publicacion'):
            if publicacion not in publicaciones:
                publicaciones.append(publicacion)

        totalVals = Valoracion.objects.filter(usuario=UsuarioPerfil.objects.get_or_create(user = self.request.user)[0])
        finalVals=[]
        
        for p in publicaciones:
            valorada = False
            for val in totalVals:
                if val.publicacion.id == p.id:
                    finalVals.append(val.puntuacion)
                    valorada = True
            if not valorada:
                finalVals.append(0)

        context['formulario_valoracion'] = ValoracionForm()
        context['publicaciones'] = list(zip(publicaciones, finalVals))
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
        publicaciones = Publicacion.objects.filter(categoria=categoria).order_by('-fecha_publicacion')

        totalVals = Valoracion.objects.filter(usuario=UsuarioPerfil.objects.get_or_create(user = self.request.user)[0])
        finalVals=[]
        for p in publicaciones:
            valorada = False
            for val in totalVals:
                if val.publicacion.id == p.id:
                    finalVals.append(val.puntuacion)
                    valorada = True
            if not valorada:
                finalVals.append(0)

        context['publicaciones'] = list(zip(publicaciones,finalVals))
        context['categorias'] = Categorias.choices()
        return context