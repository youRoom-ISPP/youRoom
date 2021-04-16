import os
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.TiendaView.as_view(),name='home'),
   path('charge/<pk>/', views.TiendaView.charge, name='charge'),
   path('cancel_suscription/', views.TiendaView.cancel_suscription, name='cancel'),
   path('cancelar_suscripcion_tienda/', views.TiendaView.cancelar_suscripcion_tienda, name='tienda_cancel')
]
