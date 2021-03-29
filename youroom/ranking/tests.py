from django.test import TestCase
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil
from ranking.models import Valoracion
from publicacion.models import Publicacion
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from publicacion.enum import Categorias
from django.urls import reverse

class ValorarTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        u = User(username='prueba')
        u.set_password('usuario1234')
        u.email = 'prueba@gmail.com'
        u.isActive = True
        u.save()
        perfil = UsuarioPerfil(user=u)
        perfil.save()
        self.usuario = perfil
        self.usuario.save()

    def tearDown(self):
        self.client = None

    def test_valorar(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        login = self.client.post('', answers)
        self.assertTemplateUsed(template_name='timeline/timeline.html')

        imagen = SimpleUploadedFile(name='test_image.png', content=open('static/images/logo-xl.png', 'rb').read())
        response = self.client.post("http://testserver{}".format(reverse("publicacion_guardar")), {
            'imagen': imagen,
            'descripcion' : "Prueba",
            'categoria' : Categorias.SALON,
            'usuario':  self.usuario,
            'format': 'multipart/form-data'},follow = True)

        answers = {
            'puntuacion':4,
            'publicacion_id':Publicacion.objects.last().id
            }

        response = self.client.post('/timeline/valorar/', answers)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/timeline/', status_code=302,
        target_status_code=200, fetch_redirect_response=True)

        objeto_guardado = Valoracion.objects.last()
        self.assertEqual(objeto_guardado.usuario.user.username,'prueba' )
        self.assertEqual(objeto_guardado.publicacion.id,Publicacion.objects.last().id)
        self.assertEqual(objeto_guardado.puntuacion,4)
