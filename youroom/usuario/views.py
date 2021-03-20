from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as auth_view

class LoginView(auth_view):
    template_name = 'usuario/login.html'
class HomeView(TemplateView):
    template_name = 'usuario/home.html'
