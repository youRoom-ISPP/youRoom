import os
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from perfil.forms import PerfilForm
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil, ContadorVida
from tienda.models import Product
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

@method_decorator(login_required, name='dispatch')
class PerfilView(TemplateView):
    template_name = 'perfil/perfil.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            usuario, create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
            cont = ContadorVida.objects.get_or_create(perfil=usuario)[0]
            product = Product.objects.get(id=1)
            # Datos necesarios para la suscripcion
            context['key'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
            context['product'] = product
            #Del contador obtienes el numVidasSemanales y el numVidasCompradas
            context['cont'] = cont
            publicaciones = Publicacion.objects.filter(usuario=usuario).order_by('-fecha_publicacion')
            context['publicaciones'] = publicaciones
            context['numPublicaciones'] = publicaciones.count()
            context['user'] = usuario
            context['vidasTotales'] = cont.numVidasCompradas + cont.numVidasSemanales
            # formulario_editar_perfil = PerfilForm()
            # formulario_editar_perfil['descripcion'] = usuario.descripcion
            # formulario_editar_perfil['password1'] = usuario.user.password
            # formulario_editar_perfil['password2'] = usuario.user.password
            context['formulario_perfil'] =  PerfilForm()
            return context
        except Exception as e:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


@method_decorator(login_required, name='dispatch')
class EditarPerfilView(FormView):
    form_class = PerfilForm
    template_name = 'perfil/editar_perfil.html'
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        try:
            usuario_perfil = UsuarioPerfil.objects.get_or_create(user=self.request.user)[0]
            usuario_perfil.descripcion = form.cleaned_data.get['descripcion']
            usuario_perfil.user.password = form.cleaned_data.get['contrasena']
            usuario=usuario_perfil.imagen = form.cleaned_data.get['imagen']
            return super().form_valid(form)
        except Exception as e:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)



