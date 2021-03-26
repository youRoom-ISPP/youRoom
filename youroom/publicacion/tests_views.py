import io, os
from PIL import Image
from rest_framework.test import  APIClient , APITestCase
from django.urls import reverse
from publicacion.models import Publicacion
from publicacion.enum import Categorias
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil

class PublicacionViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
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


    def test_publicacion_view_not_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("publicacion")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

        response = self.client.get("http://testserver{}".format(reverse("publicacion_guardar")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')



    def test_publicacion_view(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        login = self.client.post('', answers)
        response = self.client.get("http://testserver{}".format(reverse("publicacion")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='publicacion/subir_imagen.html')


    def test_subir_publicacion_view(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        login = self.client.post('', answers)
        formulario = self.client.get("http://testserver{}".format(reverse("publicacion")))
        csrftoken = formulario.cookies['csrftoken']
        imagen = self.generate_photo_file()

        perfil, create = UsuarioPerfil.objects.get_or_create(user = self.u)
        response = self.client.post("http://testserver{}".format(reverse("publicacion_guardar")), {
            'imagen': imagen,
            'descripcion' : "Prueba",
            'categoria' : Categorias.SALON,
            'usuario':  perfil,
            'format': 'multipart/form-data'},follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        objeto_guardado = Publicacion.objects.last()
        self.assertEqual(objeto_guardado.imagen.name, "publicaciones/" + imagen.name)
        self.assertEqual(objeto_guardado.categoria,'Categorias.SALON')
        self.assertEqual(objeto_guardado.descripcion,"Prueba")
        self.assertEqual(objeto_guardado.usuario, perfil)
        
        