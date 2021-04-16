import os
import stripe
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from tienda.models import Product
from django.http import HttpResponseRedirect, JsonResponse
from usuario.models import UsuarioPerfil, Premium, ContadorVida
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from publicacion.models import Publicacion

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'tienda/home.html'

    def get_context_data(self, **kwargs):
        try:
            products = Product.objects.all()
            context = super().get_context_data(**kwargs)
            context['key'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
            context['products'] = products
            return context

        except:
            message = 'Ha ocurrido un error al cargar los productos'
            return render(request, 'tienda/fail.html', {'message':message})

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

            # Comprobar los posibles errores a la hora de realizar el pago
            if estado == 'credit_card_error':
                message='Ha habido un error con el pago de su tarjeta'
                return render(request, 'tienda/fail.html', {'message':message})

            elif estado == 'invalid_request_error':
                message='Ha habido un error con la petición de pago'
                return render(request, 'tienda/fail.html', {'message':message})

            elif estado == 'error_creating_customer':
                message='Ha habido con sus datos en Stripe'
                return render(request, 'tienda/fail.html', {'message':message})

                
            elif estado == 'error':
                message='Ha habido un error desconocido'
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

        return HttpResponseRedirect('/perfil/')

    def cancel_suscription(request):
        try:
            perfil = UsuarioPerfil.objects.get_or_create(user = request.user)[0]
            premium_query = Premium.objects.filter(perfil=perfil)
            if premium_query.exists()  and premium_query[0].fechaCancelacion==None:
                premium = premium_query[0]
                customer = stripe.Customer.retrieve(perfil.id_stripe)
                suscripcion = stripe.Subscription.list(customer=customer.id)['data'][0]
                stripe.Subscription.modify(suscripcion['id'], cancel_at_period_end=True)
                premium.fechaCancelacion = date.fromtimestamp(suscripcion['current_period_end'])
                premium.save()

            return HttpResponseRedirect('/perfil/')
        
        except:
            message = 'Ha ocurrido un error al cancelar su suscripción'
            return render(request, 'tienda/fail.html', {'message':message})

    def obtiene_fecha_cancelacion(request):
        try:
            perfil = UsuarioPerfil.objects.get_or_create(user = request.user)[0]
            premium = Premium.objects.filter(perfil=perfil)

            if premium.exists()  and premium[0].fechaCancelacion==None:
                customer = stripe.Customer.retrieve(perfil.id_stripe)
                suscripcion = stripe.Subscription.list(customer=customer.id)['data'][0]
                fecha_cancelacion = date.fromtimestamp(suscripcion['current_period_end'])
                return JsonResponse({'fechaCancelacion':fecha_cancelacion,'valid':True})
            else:
                return JsonResponse({'fechaCancelacion':'','valid':False})
        
        except:
            message = 'Ha ocurrido un error al comprobar tu suscripción'
            return render(request, 'tienda/fail.html', {'message':message})

        


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
    
    except stripe.error.InvalidRequestError as e:
        return 'invalid_request_error'
    
    except:
        return 'error'

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
                "price": os.getenv('SUSCRIPTION_PRICE_KEY'),
                "quantity": 1,
                },
        ],
        )
        
        return 'success'

    except stripe.error.CardError as e:
        return 'credit_card_error'

    except stripe.error.InvalidRequestError as e:
        return 'invalid_request_error'

    except:
        return 'error'