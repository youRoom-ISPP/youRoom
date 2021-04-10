import os  
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('vidas/',views.BuyVidaView.as_view(),name='home'),
   path('charge/<pk>/', views.BuyVidaView.charge, name='charge')
]