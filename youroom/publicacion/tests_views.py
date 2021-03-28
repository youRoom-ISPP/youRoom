import io, os
from PIL import Image
from rest_framework.test import  APIClient , APITestCase
from django.urls import reverse
from publicacion.models import Publicacion, Destacada
from publicacion.enum import Categorias
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida

class PublicacionViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.isActive=True
        self.u.save()
        self.p = UsuarioPerfil.objects.get_or_create(user = self.u)[0]
        self.c= ContadorVida.objects.get_or_create(perfil=self.p,estaActivo=True)[0]
    
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

        perfil= UsuarioPerfil.objects.get_or_create(user = self.u)[0]
        cont= ContadorVida.objects.get_or_create(perfil=perfil,estaActivo=True)[0]
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

    def test_destacar_not_logged(self):
        response = self.client.get("/publicacion/destacar/1")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_destacar_logged(self):

        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        login = self.client.post('', answers)

        # Contamos la cantidad de publicaciones destacadas que tenemos inicialmente
        cantidad_destacados_inicial = Destacada.objects.all().count()

        imagen = self.generate_photo_file()
        perfil = UsuarioPerfil.objects.get_or_create(user = self.u)[0]
        cont= ContadorVida.objects.get_or_create(perfil=perfil,estaActivo=True)[0]
        response = self.client.post("http://testserver{}".format(reverse("publicacion_guardar")), {
            'imagen': imagen,
            'descripcion' : "Prueba",
            'categoria' : Categorias.SALON,
            'usuario':  perfil,
            'format': 'multipart/form-data'},follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        # Al destacar la última publicación, confirmamos que hay una publicación destacada más y que coincide
        publicacion = Publicacion.objects.last()
        response = self.client.get("/publicacion/destacar/" + str(publicacion.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        self.assertEqual(Destacada.objects.all().count(), cantidad_destacados_inicial + 1)

        ultima_destacada = Destacada.objects.last()
        self.assertEqual(ultima_destacada.publicacion, publicacion)

        # Intentamos volver a destacar una publicación destacada y no se crea otra vez

        response = self.client.get("/publicacion/destacar/" + str(publicacion.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        self.assertEqual(Destacada.objects.all().count(), cantidad_destacados_inicial + 1)


    def test_destacar_otro_usuario_logged(self):

        # Creamos nuevo usuario
        usuario2 = User.objects.get_or_create(username='prueba2', password='prueba2')[0]
        
        cantidad_destacados_inicial = Destacada.objects.all().count()
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        login = self.client.post('', answers)

        
        imagen = self.generate_photo_file()

        # Usuario 1 realiza una publicación
        response = self.client.post("http://testserver{}".format(reverse("publicacion_guardar")), {
            'imagen': imagen,
            'descripcion' : "Prueba",
            'categoria' : Categorias.SALON,
            'format': 'multipart/form-data'},follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        # Usuario 2 intenta destacar la publicación del usuario 1
        self.client.logout()
        self.client.login(username='prueba2', password='prueba2')

        publicacion = Publicacion.objects.last()
        response = self.client.get("/publicacion/destacar/" + str(publicacion.id))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        self.assertEqual(Destacada.objects.all().count(), cantidad_destacados_inicial)
        

        
        