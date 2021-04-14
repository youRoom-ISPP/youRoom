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

            # Si es una suscripción, y el usuario ya esta suscrito, rechazar suscripción
            if Premium.objects.filter(perfil=perfil).exists():
                message='Ya tiene una suscripción activa en su perfil'
                return render(request, 'tienda/fail.html', {'message':message})

            # realizar pago
            if product.numVidas == 0:
                estado = suscribirse(request, product, perfil)
            else:
                estado = pay(request, product)

            # redirigir si ha habido un error en el pago de la tarjeta
            if estado == 'credit_card_error':
                message='Ha habido un error con el pago de su tarjeta'
                return render(request, 'tienda/fail.html', {'message':message})

            elif estado == 'success':
                
                # Añadir objeto vida si se ha hecho la compra correctamente
                if product.numVidas != 0:
                    contador = ContadorVida.objects.get_or_create(perfil = perfil)[0]
                    contador.numVidasCompradas += product.numVidas
                    contador.save()

                # Crear objeto premium si se ha hecho la suscripción correctamente
                if product.numVidas == 0:
                    premium = Premium(perfil=perfil)
                    cv = ContadorVida.objects.get_or_create(perfil=perfil)[0]
                    cv.estaActivo = False
                    premium.save()
                    cv.save()
            
                return HttpResponseRedirect('/perfil/')

    def cancel_suscription(request):
        perfil = UsuarioPerfil.objects.get_or_create(user = request.user)[0]
        premium = Premium.objects.filter(perfil=perfil)

        if premium.exists()  and premium[0].fechaCancelacion==None:
            customer = stripe.Customer.retrieve(perfil.id_stripe)
            suscription_id = stripe.Subscription.list(customer=customer.id)['data'][0]['id']
            stripe.Subscription.modify(suscription_id, cancel_at_period_end=True)

            premium = Premium.objects.filter(perfil=perfil)[0]
            premium = calcula_cancelacion(request, premium)
            premium.save()

        return HttpResponseRedirect('/perfil/')


def calcula_cancelacion(request, premium):
    dia_sus = premium.fechaSuscripcion.day
    hoy = timezone.now().date().day

    if dia_sus <= hoy:
        fechaCancelacion = timezone.datetime(
            timezone.now().date().year,
            timezone.now().date().month + 1, 
            dia_sus
            )
    else:
        fechaCancelacion = timezone.datetime(
            timezone.now().date().year,
            timezone.now().date().month, 
            dia_sus
            )

    premium.fechaCancelacion = fechaCancelacion
    return premium


def pay(request, product):
    try:
        charge = stripe.Charge.create(
            amount=product.price,
            currency='EUR',
            description='Pago de ' + str(product.numVidas) + ' vidas',
            source=request.POST['stripeToken'],
        )
        
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'

def suscribirse(request, product, perfil):
    try:
        # Comprobamos que el usuario ya esté registrado en stripe

        if perfil.id_stripe == '':
            try:
                customer = stripe.Customer.create(
                    email = perfil.user.email,
                    name = perfil.user.username,
                    source = request.POST['stripeToken']
                )
                perfil.id_stripe = customer.id
                perfil.save()
            except stripe.error.StripeError as e:
                return 'error_creating_customer'


        stripe.Subscription.create(
        customer=perfil.id_stripe,
        items=[
                {
                "price":"price_1IftjiDQeZjKA2R4JbxQtvpx",
                "quantity": 1,
                },
        ],
        )
        
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'