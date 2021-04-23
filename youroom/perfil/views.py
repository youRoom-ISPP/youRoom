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
            return context
        except Exception as e:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


@method_decorator(login_required, name='dispatch')
class EditarPerfilView(FormView):
    form_class = PerfilForm
    template_name = 'perfil/editar_perfil.html'
    success_url = reverse_lazy('perfil')

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario, create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
        formulario_editar_perfil =  PerfilForm(initial={ 
            "descripcion": usuario.descripcion})
        context['formulario_perfil'] =  formulario_editar_perfil
        return render(self.request, 'perfil/editar_perfil.html', context)

    def form_valid(self,form):
        #try:
            usuario_perfil = UsuarioPerfil.objects.get_or_create(user=self.request.user)[0]
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 =='' and password2 =='':
                usuario_perfil.descripcion = form.cleaned_data['descripcion']
                usuario=usuario_perfil.imagen = form.cleaned_data['imagen']
                return super().form_valid(form)
            elif password1 != '' and password2 != '' and password1==password2:
                usuario_perfil.descripcion = form.cleaned_data['descripcion']
                usuario=usuario_perfil.imagen = form.cleaned_data['imagen']
                usuario_perfil.user.password = password1
                return super().form_valid(form)
            elif password1 != '' and password2 != '' and password1!=password2:
                context = {'error_message': 'Las contraseñas deben coincidir'}
                return render(self.request, 'base/error.html', context)
            else:
                context = {'error_message': 'Ha ocurrido un error inesperado'}
                return render(self.request, 'base/error.html', context)
        #except Exception as e:
            # context = {'error_message': 'Ha ocurrido un error inesperado'}
            # return render(self.request, 'base/error.html', context)


-------------

class EditarPerfilView(FormView):
    form_class = PerfilForm
    template_name = 'perfil/editar_perfil.html'
    success_url = reverse_lazy('perfil')

    def form_valid(self,form, **kwargs):
        try:
            descripcion = form.cleaned_data['descripcion']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            imagen = form.cleaned_data['imagen']
            usuario = getUser()
            usuario.descripcion = descripcion
            if password1 != '' and password2 != '' and password1==password2:
                usuario.user.password = password1
            return super().form_valid(form)

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

    def getUser(self, request):
        usuario, create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
        return usuario  