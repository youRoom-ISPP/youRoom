import os
import stripe
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from usuario.models import UsuarioPerfil, Premium
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@method_decorator(login_required, name='dispatch')
class SuscripcionView(TemplateView):
    template_name = 'tienda/suscripcion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = UsuarioPerfil.objects.get_or_create(user = self.request.user)[0]
        if Premium.objects.filter(perfil=perfil).exists():
            context['esPremium'] = True
        else:
            context['key'] = os.getenv('STRIPE_PUBLISHABLE_KEY')

        return context

    def charge(request):
        if request.method == 'POST':

            perfil = UsuarioPerfil.objects.get_or_create(user = request.user)[0]

            # Si es una suscripción, y el usuario ya esta suscrito, rechazar suscripción
            if Premium.objects.filter(perfil=perfil).exists():
                message='Ya tiene una suscripción activa en su perfil'
                return render(request, 'tienda/fail.html', {'message':message})

            # realizar pago
            estado = pay(request)

            # redirigir si ha habido un error en el pago de la tarjeta
            if estado == 'credit_card_error':
                message='Ha habido un error con el pago de su tarjeta'
                return render(request, 'tienda/fail.html', {'message':message})

            elif estado == 'success':

                # Crear objeto premium si se ha hecho la suscripción correctamente
                premium = Premium.objects.create(perfil=perfil)
                premium.save()

                return HttpResponseRedirect('/perfil/')


def pay(request):
    try:
        charge = stripe.Charge.create(
            amount=299,
            currency='EUR',
            description='Suscripción mensual',
            source=request.POST['stripeToken']
        )
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'
