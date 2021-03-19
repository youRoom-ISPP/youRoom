from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

class LoginView(LoginView):
    template_name = 'usuario/login.html'
class HomeView(TemplateView):
    template_name = 'usuario/home.html'