import os
import boto3
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil, ContadorVida
from tienda.models import Product
from .forms import FotoPerfilForm
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
    form_class = FotoPerfilForm
    success_url = reverse_lazy('perfil')

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
        context['foto_perfil'] = usuario.foto_perfil
        return render(self.request, 'perfil/editar_perfil.html', context)

    def borrar_foto_perfil_anterior(self, foto_perfil):
        if os.getenv('PROD') == 'True':
            s3.delete_object(Bucket=BUCKET_NAME, Key=str(foto_perfil.name))
        else:
            storage, path = foto_perfil.storage, foto_perfil.path
            storage.delete(path)

    def form_valid(self, form):
        print(self.request.FILES['imagen_recortada'].read())
        usuario = get_object_or_404(UsuarioPerfil, user=self.request.user)
        foto_perfil = form.cleaned_data['foto_perfil']
        if foto_perfil != '':
            if usuario.foto_perfil != '':
                self.borrar_foto_perfil_anterior(usuario.foto_perfil)
            usuario.foto_perfil = foto_perfil
        usuario.save()
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context = {'error_message': 'Ha ocurrido un error inesperado'}
        return render(self.request, 'perfil/editar_perfil.html', context)