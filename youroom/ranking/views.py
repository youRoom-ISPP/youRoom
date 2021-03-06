
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, TemplateView
from ranking.forms import ValoracionForm
from ranking.models import Valoracion
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil, ContadorVida
from django.shortcuts import render
from django.http import JsonResponse


@method_decorator(login_required, name='dispatch')
class ValorarPublicacionView(FormView):
    form_class = ValoracionForm
    template_name = 'timeline/timeline.html'
    success_url = reverse_lazy('timeline')

    def form_valid(self, form):
        try:
            usuario_perfil, create = UsuarioPerfil.objects.get_or_create(user=self.request.user)
            publicacion_a_valorar, create = Publicacion.objects.get_or_create(id=form.cleaned_data['publicacion_id'])
            valoracion, create = Valoracion.objects.get_or_create(
                usuario=usuario_perfil,
                publicacion=publicacion_a_valorar
            )
            if not create:
                previo = valoracion.puntuacion
                publicacion_a_valorar.usuario.totalPuntos -= previo
                publicacion_a_valorar.usuario.puntosSemanales -= previo
                publicacion_a_valorar.totalValoraciones -= previo
            puntos = int(form.cleaned_data.get('puntuacion'))
            valoracion.puntuacion = puntos
            valoracion.save()
            publicacion_a_valorar.usuario.totalPuntos += puntos
            publicacion_a_valorar.usuario.puntosSemanales += puntos
            publicacion_a_valorar.usuario.save()
            publicacion_a_valorar.totalValoraciones += puntos
            publicacion_a_valorar.save()
            return JsonResponse({'message': 'Valoración guardada correctamente', 'valid': True, 'total_valoracion': publicacion_a_valorar.totalValoraciones  })
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


class RankingView(TemplateView):
    template_name = 'ranking/ranking.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            lista_usuarios = UsuarioPerfil.objects.filter(puntosSemanales__gt=0).order_by('-puntosSemanales')
            usuario_logueado = UsuarioPerfil.objects.get(user=self.request.user)
            contador_usuario_logueado = ContadorVida.objects.get(perfil=usuario_logueado)
            context['cont'] = contador_usuario_logueado
            if lista_usuarios.count() > 50:
                context['usuarios'] = lista_usuarios[:50]
            else:
                context['usuarios'] = lista_usuarios
            return context
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)
