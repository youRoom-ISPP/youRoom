from django.utils import timezone
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import PublicacionForm
from .models import Publicacion


class PublicacionView(TemplateView):
    template_name = 'publicacion/subir_imagen.html'

    def get_context_data(self, **kwargs):
        context = super(PublicacionView, self).get_context_data(**kwargs)
        context['formulario_imagen'] = PublicacionForm()
        return context


class SubirPublicacionView(FormView):
    form_class = PublicacionForm
    template_name = 'publicacion/subir_imagen.html'
    success_url = reverse_lazy('publicacion')

    def form_valid(self, form):
        publicacion = Publicacion.objects.create()
        publicacion.imagen = form.cleaned_data['imagen']
        publicacion.fecha_subida = timezone.now()
        publicacion.save()
        return super().form_valid(form)
