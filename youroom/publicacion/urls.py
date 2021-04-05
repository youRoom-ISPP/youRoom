from django.urls import path
from .views import PublicacionView, SubirPublicacionView, DestacarPublicacionView

urlpatterns = [
    path('', PublicacionView.as_view(), name='publicacion'),
    path('subir/', SubirPublicacionView.as_view(), name='publicacion_guardar'),
    path('destacar/<publicacion_id>', DestacarPublicacionView.as_view(), name='destacar_publicacion'),
]
