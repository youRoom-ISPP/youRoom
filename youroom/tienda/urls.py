from django.urls import path
from tienda.views import CreateCheckoutSessionView, ProductLandingPageView

urlpatterns = [
    path('vidas/', ProductLandingPageView.as_view(), name='landing_page')
   # path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session')


]