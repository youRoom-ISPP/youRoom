import os
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.TiendaView.as_view(), name='tienda'),
   path('pago/<pk>/', views.TiendaView.charge, name='charge'),
   path('cancelar_suscripcion/', views.TiendaView.cancelar_suscripcion, name='cancelar'),
   path('obtener_fecha_cancelacion/', views.TiendaView.obtener_fecha_cancelacion, name='obtener_fecha')
]
