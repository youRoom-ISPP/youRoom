import os
import boto3
from django.shortcuts import render, get_object_or_404
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
from dotenv import load_dotenv

load_dotenv()
BUCKET_NAME = os.environ.get("S3_BUCKET")
s3 = boto3.client('s3')

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
        usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
        formulario_editar_perfil = PerfilForm(initial={
            "descripcion": usuario.descripcion})
        context['form'] = formulario_editar_perfil
        context['imagen'] = usuario.foto_perfil
        return render(self.request, 'perfil/editar_perfil.html', context)

    def borrar_imagen_anterior(self, imagen):
        if os.getenv('PROD') == 'True':
            s3.delete_object(Bucket=BUCKET_NAME, Key=str(imagen.name))
        else:
            storage, path = imagen.storage, imagen.path
            storage.delete(path)

    def form_valid(self, form):
        usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
        imagen = form.cleaned_data['imagen']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        usuario.descripcion = form.cleaned_data['descripcion']
        if imagen != '':
            if usuario.foto_perfil != '':
                self.borrar_imagen_anterior(usuario.foto_perfil)
            usuario.foto_perfil = imagen
        usuario.save()
        if password1 != '' and password2 != '' and password1 == password2:
            usuario.user.set_password(password1)
            usuario.user.save()
            user = authenticate(username=usuario.user.username, password=password1)
            login(self.request, user)
        elif password1 != '' or password2 != '' or password1 != password2:
            return super().form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['error_message'] = 'Ha ocurrido un error inesperado'
        return render(self.request, 'perfil/editar_perfil.html', context)

            


