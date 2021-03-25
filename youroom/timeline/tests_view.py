from django.test import TestCase
import io, os
from PIL import Image
from rest_framework.test import  APIClient , APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from publicacion.enum import Categorias
from usuario.models import UsuarioPerfil

# Create your tests here.

class TimelineViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('prueba')
        self.u.email = 'prueba@gmail.com'
        self.u.isActive=True
        self.u.save()
    
    def tearDown(self):
        self.client = None
        if os.path.exists('./media/publicaciones/test.png') :
            os.remove('./media/publicaciones/test.png')


    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_timeline_no_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_timeline_categoria_no_logged(self):
        response = self.client.get('/timeline/Dormitorio')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')


    def test_timeline_categoria_logged(self):
        # El usuario se loguea y accede a su perfil
        self.client.login(username='prueba', password='prueba')

        response = self.client.get('/timeline/Dormitorio')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='timeline/timeline.html')
    

    def test_timeline_logged(self):
        # El usuario se loguea y accede a su perfil
        self.client.login(username='prueba', password='prueba')

        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='timeline/timeline.html')

    def test_timeline_new_publicacion_logged(self):

        self.client.login(username='prueba', password='prueba')

        # El usuario entra a la Timeline y no ve ninguna publicación
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 0)

        # El usuario entra a la categoría Dormitorio y no ve ninguna publicación
        response = self.client.get('/timeline/Dormitorio')
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 0)

        # El usuario realiza una publicación de la categoría Dormitorio
        formulario = self.client.get("http://testserver{}".format(reverse("publicacion")))
        self.assertEqual(response.status_code, 200)

        csrftoken = formulario.cookies['csrftoken']
        imagen = self.generate_photo_file()
        perfil, create = UsuarioPerfil.objects.get_or_create(user = self.u)
        response = self.client.post("http://testserver{}".format(reverse("publicacion_guardar")), {
            'imagen': imagen,
            'descripcion' : "Prueba",
            'categoria' :  Categorias.DORMITORIO,
            'usuario':  perfil,
            'format': 'multipart/form-data'},follow = True)
        self.assertEqual(response.status_code, 200)

        # El usuario entra a la Timeline y encuentra una publicación
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 1)
        self.assertEqual(publicaciones[0].categoria, str(Categorias.DORMITORIO))

        # El usuario entra a la categoría Escritorio y no encuentra ninguna publicación
        response = self.client.get('/timeline/Escritorio')
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 0)

        # El usuario entra a la categoría Dormitorio y encuentra una publicación
        response = self.client.get('/timeline/Dormitorio')
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 1)
        self.assertEqual(publicaciones[0].categoria, str(Categorias.DORMITORIO))








    