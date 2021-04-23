import os
from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.views.generic.edit import UpdateView
from perfil.forms import PerfilForm
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil, ContadorVida
from tienda.models import Product
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login

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
    template_name = 'perfil/editar_perfil.html'
    form_class = PerfilForm
    success_url = reverse_lazy('perfil')


    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario, create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
        formulario_editar_perfil =  PerfilForm(initial={ 
            "descripcion": usuario.descripcion})
        context['form'] =  formulario_editar_perfil
        return render(self.request, 'perfil/editar_perfil.html', context)

    def post(self, request, *args, **kwargs):
        usuario, create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
        username = usuario.user.username
        form = PerfilForm(request.POST)
        if form.is_valid():
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']
            usuario.descripcion = form.cleaned_data['descripcion']
            if password1 != '' and password2 != '' and password1==password2:
                usuario.user.set_password(password1)
                usuario.user.save()
                user = authenticate(username=username, password=password1)
                login(request,user)
            elif password1 != '' or password2 != '' or password1!=password2:
                return super().form_invalid(form)
            usuario.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().form_valid(form)


    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context = {'error_message': 'Ha ocurrido un error inesperado'}
        return render(self.request, 'perfil/editar_perfil.html', context)

            


