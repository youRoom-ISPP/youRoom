from django.urls import path
from .views import PerfilView, EditarPerfilView

urlpatterns = [
    path('', PerfilView.as_view(), name='perfil'),
    path('editar_perfil/',EditarPerfilView.as_view(),name='editar_perfil'),
    path('editar_perfil/',EditarPerfilView.as_view(),name='guardar_perfil'),
]