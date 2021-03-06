from django.shortcuts import render
from publicacion.models import Publicacion, Destacada, Comentario
from ranking.forms import ValoracionForm
from ranking.models import Valoracion
from usuario.models import UsuarioPerfil
from publicacion.enum import Categorias
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.views.generic.list import ListView


@method_decorator(login_required, name='dispatch')
class TimelineView(ListView):
    template_name = 'timeline/timeline.html'
    paginate_by = 5
    context_object_name = 'publicaciones'

    def get_queryset(self):
        try:
            publicaciones = []
            for destacada in Destacada.objects.all():
                if (datetime.now(timezone.utc) - destacada.fecha_destacada).total_seconds() > 86400:
                    destacada.delete()
                else:
                    publicaciones.append(destacada.publicacion)

            publicaciones.sort(key=lambda x: x.fecha_publicacion, reverse=True)

            for publicacion in Publicacion.objects.all().order_by('-fecha_publicacion'):
                if publicacion not in publicaciones:
                    publicaciones.append(publicacion)

            totalVals = Valoracion.objects.filter(usuario=UsuarioPerfil.objects.get_or_create(user = self.request.user)[0])
            finalVals=[]
            comentarios = Comentario.objects.all()
            finalComents = []
            for p in publicaciones:
                valorada = False
                for val in totalVals:
                    if val.publicacion.id == p.id:
                        finalVals.append(val.puntuacion)
                        valorada = True
                if not valorada:
                    finalVals.append(0)
                aux = []
                for comentario in comentarios:
                    if comentario.publicacion.id == p.id:
                        aux.append(comentario)
                aux = aux[:2]
                finalComents.append(aux)
            publicaciones = list(zip(publicaciones, finalVals, finalComents))
            return publicaciones

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['formulario_valoracion'] = ValoracionForm()
            context['categorias'] = Categorias.choices()

            return context

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


@method_decorator(login_required, name='dispatch')
class TimelineViewValoraciones(ListView):
    template_name = 'timeline/timeline.html'
    paginate_by = 5
    context_object_name = 'publicaciones'

    def get_queryset(self):
        try:
            publicaciones = []

            for publicacion in Publicacion.objects.all().order_by('-totalValoraciones'):
                if publicacion not in publicaciones:
                    publicaciones.append(publicacion)

            totalVals = Valoracion.objects.filter(usuario=UsuarioPerfil.objects.get_or_create(user = self.request.user)[0])
            finalVals = []

            comentarios = Comentario.objects.all()
            finalComents = []
            for p in publicaciones:
                valorada = False
                for val in totalVals:
                    if val.publicacion.id == p.id:
                        finalVals.append(val.puntuacion)
                        valorada = True
                if not valorada:
                    finalVals.append(0)
                aux = []
                for comentario in comentarios:
                    if comentario.publicacion.id == p.id:
                        aux.append(comentario)
                aux = aux[:2]
                finalComents.append(aux)
            return list(zip(publicaciones, finalVals, finalComents))

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['formulario_valoracion'] = ValoracionForm()
            context['categorias'] = Categorias.choices()

            return context

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


@method_decorator(login_required, name='dispatch')
class TimelineViewCategorias(ListView):
    template_name = 'timeline/timeline.html'
    paginate_by = 5
    context_object_name = 'publicaciones'

    def get_queryset(self):
        try:
            categoria_seleccionada = self.kwargs.get('categoria')

            categoria = None
            for tupla in Categorias.choices():
                if tupla[1] == categoria_seleccionada:
                    categoria = tupla[0]
                    break
            publicaciones = Publicacion.objects.filter(categoria=categoria).order_by('-fecha_publicacion')
            comentarios = Comentario.objects.all().order_by('-fecha')
            finalComents = []

            totalVals = Valoracion.objects.filter(usuario=UsuarioPerfil.objects.get_or_create(user=self.request.user)[0])
            finalVals = []
            for p in publicaciones:
                valorada = False
                for val in totalVals:
                    if val.publicacion.id == p.id:
                        finalVals.append(val.puntuacion)
                        valorada = True
                if not valorada:
                    finalVals.append(0)
                aux = []
                for comentario in comentarios:
                    if comentario.publicacion.id == p.id:
                        aux.append(comentario)
                aux = aux[:2]
                finalComents.append(aux)
            return list(zip(publicaciones, finalVals, finalComents))

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            categoria_seleccionada = self.kwargs.get('categoria')
            context['categorias'] = Categorias.choices()
            context['categoria'] = categoria_seleccionada
            return context
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)
