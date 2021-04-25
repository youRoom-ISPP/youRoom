import io
import os
from PIL import Image
from django.urls import reverse
from django.core.management import call_command
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida


class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.isActive = True
        self.u.save()
        self.p = UsuarioPerfil.objects.get_or_create(user=self.u, totalPuntos=100, descripcion ='descripcion prueba')[0]
        self.c = ContadorVida.objects.get_or_create(perfil=self.p, estaActivo=True)[0]
        call_command('loaddata', 'products.json', verbosity=0)

    def tearDown(self):
        self.client = None
        if os.path.exists('./static/media/publicaciones/'):
            filelist = [f for f in os.listdir('./static/media/publicaciones/') if f.endswith(".png")]
            for f in filelist:
                os.remove(os.path.join('./static/media/publicaciones/', f))

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def publicar(self, usuario, categoria):
        self.imagen = self.generate_photo_file()
        response = self.client.post("http://testserver{}".format(reverse("publicacion_guardar")), {
            'imagen': self.imagen,
            'descripcion': "Prueba",
            'categoria': categoria,
            'usuario':  usuario,
            'format': 'multipart/form-data'}, follow=True)
        return response
