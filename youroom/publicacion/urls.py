from django.urls import path
from publicacion import views

urlpatterns = [
    path('form_publicacion/', views.PublicacionView.create_formulario_publicacion),
    path('publicacion_realizada/', views.PublicacionView.publicado_exito)
]