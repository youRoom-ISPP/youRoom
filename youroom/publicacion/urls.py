from django.urls import path
from publicacion import views

urlpatterns = [
    path('form_publicacion/', views.create_formulario_publicacion),
    path('publicacion_realizada/', views.publicado_exito)
]