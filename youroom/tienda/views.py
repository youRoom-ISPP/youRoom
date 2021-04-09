import os
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from tienda.models import Product
from usuario.models import UsuarioPerfil, Premium
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import stripe


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

            # Si es una suscripción, y el usuario ya esta suscrito, rechazar suscripción
            if product.name == 'suscripcion' and Premium.objects.filter(perfil=perfil).exists():
                message='Ya tiene una suscripción activa en su perfil'
                return render(request, 'tienda/fail.html', {'message':message})

            # realizar pago
            estado = pay(request, product)

            # redirigir si ha habido un error en el pago de la tarjeta
            if estado == 'credit_card_error':
                message='Ha habido un error con el pago de su tarjeta'
                return render(request, 'tienda/fail.html', {'message':message})

            elif estado == 'success':
                
                # Crear objeto premium si se ha hecho la suscripción correctamente
                if product.name == 'suscripcion':
                    premium = Premium.objects.create(perfil=perfil)
                    premium.save()
                    
            
                return render(request, 'tienda/charge.html')

@method_decorator(login_required, name='dispatch')
def pay(request, product):
    try:
        charge = stripe.Charge.create(
            amount=product.price,
            currency='EUR',
            description='Payment Gateway',
            source=request.POST['stripeToken']
        )
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'
