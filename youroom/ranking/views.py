
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView
from ranking.forms import ValoracionForm
from ranking.models import Valoracion
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse


@method_decorator(login_required, name='dispatch')
class ValorarPublicacionView(FormView):
    form_class = ValoracionForm
    template_name = 'timeline/timeline.html'
    success_url = reverse_lazy('timeline')
    def form_valid(self, form):
        usuario_perfil , create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
        publicacion_a_valorar , create = Publicacion.objects.get_or_create(id = form.cleaned_data['publicacion_id'])
        valoracion , create = Valoracion.objects.get_or_create(
            usuario=usuario_perfil,
            publicacion=publicacion_a_valorar
        )
        if not create:
            previo = valoracion.puntuacion
            usuario_perfil.totalPuntos -= previo
            publicacion_a_valorar.totalValoraciones -= previo
        puntos = int(form.cleaned_data.get('puntuacion'))
        valoracion.puntuacion = puntos
        valoracion.save()
        usuario_perfil.totalPuntos += puntos
        usuario_perfil.save()
        publicacion_a_valorar.totalValoraciones += puntos
        publicacion_a_valorar.save()
        return JsonResponse({'message':'Create Successfully','valid':True})


class RankingView(TemplateView):
    template_name = 'ranking/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = User.objects.all()
        return context

