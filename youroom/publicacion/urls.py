from django.urls import path
from .views import PublicacionView, SubirPublicacionView

urlpatterns = [
    path('', PublicacionView.as_view(), name='publicacion'),
    path('subir/', SubirPublicacionView.as_view(), name='publicacion_guardar'),
]
