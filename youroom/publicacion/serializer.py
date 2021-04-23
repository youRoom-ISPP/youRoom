from rest_framework import serializers
from .models import Comentario, Publicacion
from usuario.serializers import UsuarioSerializer

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = ['id']
class ComentarioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    publicacion = PublicacionSerializer(read_only=True)
    class Meta:
        model = Comentario
        fields = ['publicacion','texto', 'usuario','fecha']