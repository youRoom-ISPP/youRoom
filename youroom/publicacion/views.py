from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import PublicacionForm
from .models import Publicacion
from usuario.models import UsuarioPerfil
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class PublicacionView(TemplateView):
    template_name = 'publicacion/publicacion.html'

    def get_context_data(self, **kwargs):
        context = super(PublicacionView, self).get_context_data(**kwargs)
        context['formulario_imagen'] = PublicacionForm()
        return context


@method_decorator(login_required, name='dispatch')
class SubirPublicacionView(FormView):
    form_class = PublicacionForm
    template_name = 'publicacion/publicacion.html'
    success_url = reverse_lazy('publicacion')

    def form_valid(self, form):
        publicacion = Publicacion.objects.create()
        publicacion.imagen = form.cleaned_data['imagen']
        publicacion.categoria = form.cleaned_data.get('categoria')
        publicacion.descripcion = form.cleaned_data.get('descripcion')
        usuario_perfil , create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
        publicacion.usuario = usuario_perfil
        publicacion.save()
        return super().form_valid(form)
