import os
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from tienda.models import Vida
from usuario.models import UsuarioPerfil, Premium, ContadorVida
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@method_decorator(login_required, name='dispatch')
class BuyVidaView(TemplateView):
    template_name = 'tienda/buy_vidas.html'

    def get_context_data(self, **kwargs):
        vidas = Vida.objects.all()
        context = super().get_context_data(**kwargs)
        context['key'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
        context['vidas'] = vidas
        return context

    def charge(request, pk):
        if request.method == 'POST':

            perfil = UsuarioPerfil.objects.get_or_create(user = request.user)[0]
            vida = Vida.objects.get(id=pk)

            if Premium.objects.filter(perfil=perfil).exists():
                message='El usuario es premium, con lo que no puede tener activado el contador.'
                return render(request, 'tienda/fail.html', {'message':message})

            # realizar pago
            estado = pay(request, vida)

            # redirigir si ha habido un error en el pago de la tarjeta
            if estado == 'credit_card_error':
                message='Ha habido un error con el pago de su tarjeta'
                return render(request, 'tienda/fail.html', {'message':message})

            elif estado == 'success':
                
                # Añadir objeto vida si se ha hecho la compra correctamente
                if vida.name == 'vida1':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 1
                    contador.save()
                
                if vida.name == 'vida2':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 3
                    contador.save()
                
                if vida.name == 'vida3':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 5
                    contador.save()
                
                if vida.name == 'vida4':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 10
                    contador.save()
            
                return render(request, 'tienda/charge.html')


def pay(request, vida):
    try:
        charge = stripe.Charge.create(
            amount=vida.price,
            currency='EUR',
            description='Payment Gateway',
            source=request.POST['stripeToken']
        )
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'