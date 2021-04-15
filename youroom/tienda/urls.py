import os
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.HomePageView.as_view(),name='home'),
   path('pago/<pk>/', views.HomePageView.charge, name='charge'),
   path('cancelar_suscripcion/', views.HomePageView.cancel_suscription, name='cancel'),
   path('obtener_fecha_cancelacion/',views.HomePageView.obtiene_fecha_cancelacion, name='obtieneFecha')
]