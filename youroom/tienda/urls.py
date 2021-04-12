import os
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('suscripcion/',views.SuscripcionView.as_view(), name='suscripcion'),
   path('suscripcion/pagar', views.SuscripcionView.charge, name='charge')
]