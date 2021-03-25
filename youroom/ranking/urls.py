from django.urls import path
from .views import ValorarPublicacionView


urlpatterns = [
    path('valorar/', ValorarPublicacionView.as_view(), name='publicacion_valorar'),
]
