import io
import os
from PIL import Image
from django.urls import reverse
from publicacion.enum import Categorias
from youroom.base_tests import BaseTestCase


class PerfilViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        self.client = None
        if os.path.exists('./media/publicaciones/test.png'):
            os.remove('./media/publicaciones/test.png')

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_perfil_no_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("perfil")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_perfil_logged(self):

        # El usuario se loguea y accede a su perfil
        self.client.login(username='prueba', password='usuario1234')

        response = self.client.get("http://testserver{}".format(reverse("perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        # Su perfil es el indicado y no tiene publicaciones hechas
        perfil = response.context['user']
        publicaciones = response.context['publicaciones']

        self.assertEqual(perfil.user, self.u)
        self.assertEqual(len(publicaciones), 0)

        # El usuario realiza publicación, y al acceder a su perfil obtiene la publicación
        self.assertEqual(response.status_code, 200)

        imagen = self.generate_photo_file()

        response = self.client.post("http://testserver{}".format(reverse("publicacion_guardar")), {
            'imagen': imagen,
            'descripcion': "Prueba",
            'categoria': Categorias.SALON,
            'usuario':  self.p,
            'format': 'multipart/form-data'}, follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.get("http://testserver{}".format(reverse("perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        perfil = response.context['user']
        publicaciones = response.context['publicaciones']

        self.assertEqual(perfil.user, self.u)
        self.assertEqual(len(publicaciones), 1)
        self.assertEqual(publicaciones[0].usuario, perfil)
