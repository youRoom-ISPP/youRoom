import os  
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('',views.HomePageView.as_view(),name='home'),
   path('charge/<pk>/', views.HomePageView.charge, name='charge')
]