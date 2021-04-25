import os
import boto3
import uuid
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil, ContadorVida
from tienda.models import Product
from .forms import EditarPerfilForm
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
            usuario, create = UsuarioPerfil.objects.get_or_create(user=self.request.user)
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
        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)


@method_decorator(login_required, name='dispatch')
class EditarPerfilView(FormView):
    template_name = 'perfil/editar_perfil.html'
    form_class = EditarPerfilForm
    success_url = reverse_lazy('perfil')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
        formulario_editar_perfil = EditarPerfilForm(initial={"descripcion": usuario.descripcion})
        context['formulario_editar_perfil'] = formulario_editar_perfil
        context['foto_perfil'] = usuario.foto_perfil
        return context

    def borrar_foto_perfil_anterior(self, foto_perfil):
        if os.getenv('PROD') == 'True':
            s3.delete_object(Bucket=BUCKET_NAME, Key=str(foto_perfil.name))
        else:
            storage, path = foto_perfil.storage, foto_perfil.path
            storage.delete(path)

    def form_valid(self, form):
        if self.request.FILES.get('imagen_recortada'):
            blob_file = self.request.FILES['imagen_recortada']
            usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
            if usuario.foto_perfil != '':
                self.borrar_foto_perfil_anterior(usuario.foto_perfil)
            usuario.foto_perfil.save(usuario.user.username+str(uuid.uuid4()), blob_file)
            usuario.save()
            return JsonResponse({'message': 'Foto de perfil guardada', 'valid': True})
        else:
            usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            usuario.descripcion = form.cleaned_data['descripcion']
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
        context = {'error_message': 'Ha ocurrido un error inesperado'}
        return render(self.request, 'perfil/editar_perfil.html', context)
