import os
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from tienda.models import Product
from django.http import HttpResponseRedirect
from usuario.models import UsuarioPerfil, Premium, ContadorVida
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import stripe
from django.utils import timezone

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'tienda/home.html'

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        context = super().get_context_data(**kwargs)
        context['key'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
        context['products'] = products
        return context

    def charge(request, pk):
        if request.method == 'POST':

            perfil = UsuarioPerfil.objects.get_or_create(user = request.user)[0]
            product = Product.objects.get(id=pk)

            if (product.name == 'vida1' or product.name == 'vida2' or product.name == 'vida3' or product.name == 'vida4') and Premium.objects.filter(perfil=perfil).exists():
                message='El usuario es premium, con lo que no puede tener activado el contador.'
                return render(request, 'tienda/fail.html', {'message':message})

            # Si es una suscripción, y el usuario ya esta suscrito, rechazar suscripción
            if product.name == 'suscripcion' and Premium.objects.filter(perfil=perfil).exists():
                message='Ya tiene una suscripción activa en su perfil'
                return render(request, 'tienda/fail.html', {'message':message})

            # realizar pago
           # estado = pay(request, product)
            estado = suscribirse(request, product, perfil)

            # redirigir si ha habido un error en el pago de la tarjeta
            if estado == 'credit_card_error':
                message='Ha habido un error con el pago de su tarjeta'
                return render(request, 'tienda/fail.html', {'message':message})

            elif estado == 'success':
                
                # Añadir objeto vida si se ha hecho la compra correctamente
                if product.name == 'vida1':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 1
                    contador.save()
                
                if product.name == 'vida2':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 3
                    contador.save()
                
                if product.name == 'vida3':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 5
                    contador.save()
                
                if product.name == 'vida4':
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += 10
                    contador.save()

                # Crear objeto premium si se ha hecho la suscripción correctamente
                if product.name == 'suscripcion':
                    premium = Premium(perfil=perfil)
                    cv = ContadorVida.objects.get_or_create(perfil=perfil)[0]
                    cv.estaActivo = False
                    premium.save()
                    cv.save()
            
                return HttpResponseRedirect('/perfil/')


def pay(request, product):
    try:
        charge = stripe.Charge.create(
            amount=product.price,
            currency='EUR',
            description='Payment Gateway',
            source=request.POST['stripeToken'],
            invoice_item='price_1Ie0pPDQeZjKA2R4jxF19gqE'
        )
        
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'

def suscribirse(request, product, perfil):
    try:
        stripe.SubscriptionSchedule.create(
        customer="cus_JIRGQK7T3KvNSI",
        start_date=timezone.now(),
        end_behavior="cancel",
        phases=[
            {
            "items": [
                {
                "price":
                "price_1Ie0pPDQeZjKA2R4jxF19gqE",
                "quantity": 1,
                },
            ],
            "iterations": 1,
            },
        ],
        )
        
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'