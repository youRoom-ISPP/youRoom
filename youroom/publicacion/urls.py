from django.urls import path
from .views import PublicacionView, SubirPublicacionView, DestacarPublicacionView, ComentarPublicacionView

urlpatterns = [
    path('', PublicacionView.as_view(), name='publicacion'),
    path('subir/', SubirPublicacionView.as_view(), name='publicacion_guardar'),
    path('destacar/<publicacion_id>', DestacarPublicacionView.as_view(), name='destacar_publicacion'),
    path('comentar/', ComentarPublicacionView.as_view(), name='comentar_publicacion')
]
