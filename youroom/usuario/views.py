import json
import math
from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView as auth_view
from django.contrib.auth.models import User
from .models import UsuarioPerfil, ContadorVida, Premium
from publicacion.models import Publicacion, Comentario
from .forms import RegistroForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models.functions import Lower
from usuario.serializers import UsuarioSerializer
from datetime import datetime
from ranking.forms import ValoracionForm
from ranking.models import Valoracion
from django.views.generic.list import ListView


class LoginView(auth_view):
    template_name = 'usuario/login.html'
    redirect_authenticated_user = True


class RegistroView(FormView):
    form_class = RegistroForm
    template_name = 'usuario/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            descripcion = form.cleaned_data['descripcion']
            if password1 == password2:
                if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    perfil = UsuarioPerfil(user=user, descripcion=descripcion)
                    perfil.save()
                    cv = ContadorVida(perfil=perfil)
                    cv.save()
                    return super().form_valid(form)
                else:
                    context = self.get_context_data(form=form)
                    return self.render_to_response(context)
            else:
                context = self.get_context_data(form=form)
                return self.render_to_response(context)
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


class ShedulerJob():

    def restablecer_vidas():
        fecha_hoy = datetime.today()
        if fecha_hoy.weekday() == 0 and fecha_hoy.hour == 0 and fecha_hoy.minute == 0:
            for contador in ContadorVida.objects.all():
                contador.numVidasSemanales = 3
                contador.save()

    def restablecer_puntos_ranking():
        fecha_hoy = datetime.today()
        if fecha_hoy.weekday() == 0 and fecha_hoy.hour == 0 and fecha_hoy.minute == 0:
            ShedulerJob.recompensar_mejor_usuario()
            ShedulerJob.recompensar_resto_usuarios()
            for usuario in UsuarioPerfil.objects.all():
                usuario.puntosSemanales = 0
                usuario.save()

    def recompensar_mejor_usuario():
        mejor_usuario = UsuarioPerfil.objects.order_by('-puntosSemanales').first()
        if mejor_usuario is not None:
            if mejor_usuario.puntosSemanales > 0:
                contador_vidas = ContadorVida.objects.get(perfil=mejor_usuario)
                if contador_vidas.estaActivo is True:
                    contador_vidas.numVidasCompradas += 2
                    contador_vidas.save()
                else:
                    mejor_usuario.totalPuntos += math.ceil(0.1 * mejor_usuario.totalPuntos)
                    mejor_usuario.save()

    def recompensar_resto_usuarios():
        resto_usuarios = UsuarioPerfil.objects.order_by('-puntosSemanales')[1:3]
        if len(resto_usuarios) > 0:
            for usuario in resto_usuarios:
                if usuario.puntosSemanales > 0:
                    contador_vidas = ContadorVida.objects.get(perfil=usuario)
                    if contador_vidas.estaActivo is True:
                        contador_vidas.numVidasCompradas += 1
                        contador_vidas.save()
                    else:
                        usuario.totalPuntos += math.ceil(0.05 * usuario.totalPuntos)
                        usuario.save()

    def cancelar_suscripcion():
        fecha_hoy = datetime.today()
        if fecha_hoy.hour == 0 and fecha_hoy.minute == 0:
            for premium in Premium.objects.filter(fechaCancelacion=fecha_hoy.date()):
                perfil = premium.perfil
                premium.delete()
                contador_vidas = get_object_or_404(ContadorVida, perfil=perfil)
                contador_vidas.estaActivo = True
                contador_vidas.save()


@method_decorator(login_required, name='dispatch')
class UsuariosView(TemplateView):
    template_name = 'usuario/usuarios.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            lista_usuarios = UsuarioPerfil.objects.all().order_by(Lower('user__username'))
            serializer = UsuarioSerializer(lista_usuarios, many=True)
            context['usuarios'] = json.dumps(serializer.data)
            return context
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

@method_decorator(login_required, name='dispatch')
class UsuarioShowView(ListView):
    template_name = 'usuario/usuario.html'
    paginate_by = 5
    context_object_name = 'publicaciones'

    def get(self, request, *args, **kwargs):
        try:
            if not User.objects.filter(username=kwargs['username']).exists():
                raise Exception("El usuario no existe")
            if kwargs['username'] == self.request.user.username:
                return HttpResponseRedirect('/perfil/')
            return super(UsuarioShowView, self).get(request, kwargs['username'])
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

    def get_queryset(self):
        try:
            username = self.kwargs.get('username')
            user = User.objects.get(username=username)
            perfil = UsuarioPerfil.objects.get(user=user)
            publicaciones = Publicacion.objects.filter(usuario=perfil).order_by('-fecha_publicacion')
            totalVals = Valoracion.objects.filter(usuario=UsuarioPerfil.objects.get_or_create(user=self.request.user)[0])
            finalVals = []

            comentarios = Comentario.objects.all().order_by('-fecha')
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
            publicaciones=list(zip(publicaciones, finalVals, finalComents))
            return publicaciones
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            username = self.kwargs.get('username')
            user = User.objects.get(username=username)
            perfil = UsuarioPerfil.objects.get(user=user)
            publicaciones = Publicacion.objects.filter(usuario=perfil)
            context['formulario_valoracion'] = ValoracionForm()
            context['numPublicaciones'] = publicaciones.count()
            context['user'] = perfil

            return context

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


class PoliticaDatosView(TemplateView):
    template_name = 'rgpd/datos.html'