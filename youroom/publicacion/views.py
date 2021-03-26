from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import PublicacionForm
from .models import Publicacion, Etiqueta
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
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        usuario_perfil , create = UsuarioPerfil.objects.get_or_create(user = self.request.user)
        publicacion = Publicacion.objects.create(
            usuario=usuario_perfil,
            imagen=form.cleaned_data['imagen'],
            categoria=form.cleaned_data.get('categoria'),
            descripcion=form.cleaned_data.get('descripcion')
        )
        etiquetas = form.cleaned_data.get('etiquetas')
        if etiquetas != '':
            etiquetas_list = etiquetas.split("|")
            i = 1
            for e in etiquetas_list:
                etiqueta_elemento = e.split(",")
                Etiqueta.objects.create(
                    nombre="e-" + str(publicacion.id) + "-" + str(i),
                    enlace=etiqueta_elemento[0],
                    coord_x=float(etiqueta_elemento[1]),
                    coord_y=float(etiqueta_elemento[2]),
                    publicacion=publicacion
                )
        return super().form_valid(form)
