import os
from django.shortcuts import render
from django.views.generic import TemplateView
from publicacion.models import Publicacion
from usuario.models import UsuarioPerfil, ContadorVida
from tienda.models import Product
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
