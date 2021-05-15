from django.urls import path
from .views import LoginView, RegistroView, UsuariosView, UsuarioShowView, AyudaView, PoliticaDatosView
from django.contrib.auth.views import logout_then_login
from timeline import urls as timeline_urls
from django.urls import include

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('', include(timeline_urls)),
    path('logout/', logout_then_login, name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('usuarios/', UsuariosView.as_view(), name='usuarios'),
    path('usuarios/<username>/', UsuarioShowView.as_view(), name='usuario'),
    path('guia-usuario/', AyudaView.as_view(), name='ayuda'),
    path('politica-datos/', PoliticaDatosView.as_view(), name='politica-datos'),
]
