  
from django.contrib import admin
from django.urls import path
from tienda.views import (
    CreateCheckoutSessionView,
    ProductLandingPageView,
    SuccessView,
    CancelView,
    stripe_webhook,
    StripeIntentView
)

urlpatterns = [
   
]