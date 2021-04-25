from django.urls import reverse
from publicacion.models import Publicacion, Destacada, Comentario
from publicacion.enum import Categorias
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida, Premium
from youroom.base_tests import BaseTestCase


class PublicacionViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.u2 = User(username='prueba3')
        self.u2.set_password('usuario1234')
        self.u2.email = 'prueba3@gmail.com'
        self.u2.isActive = True
        self.u2.save()
        self.p2 = UsuarioPerfil.objects.get_or_create(user=self.u2, totalPuntos=100)[0]
        self.c2 = ContadorVida.objects.get_or_create(perfil=self.p2, estaActivo=True)[0]

    def tearDown(self):
        super().tearDown()

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
        self.client.post('', answers)
        response = self.client.get("http://testserver{}".format(reverse("publicacion")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='publicacion/subir_imagen.html')

    def test_subir_publicacion_view(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        self.client.post('', answers)
        response = super().publicar(self.p, Categorias.SALON)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        cont = ContadorVida.objects.get(perfil=self.p)
        self.assertEqual(cont.numVidasSemanales, 2)

        objeto_guardado = Publicacion.objects.last()
        self.assertEqual(objeto_guardado.imagen.name, "publicaciones/" + self.imagen.name)
        self.assertEqual(objeto_guardado.categoria, 'Categorias.SALON')
        self.assertEqual(objeto_guardado.descripcion, "Prueba")
        self.assertEqual(objeto_guardado.usuario, self.p)

    def test_destacar_not_logged(self):
        response = self.client.get("/publicacion/destacar/1")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_destacar_logged(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        self.client.post('', answers)

        # Contamos la cantidad de publicaciones destacadas que tenemos inicialmente
        cantidad_destacados_inicial = Destacada.objects.all().count()
        response = super().publicar(self.p, Categorias.SALON)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        # Al destacar la última publicación, confirmamos que hay una publicación destacada más y que coincide
        publicacion = Publicacion.objects.last()

        response = self.client.get("/publicacion/destacar/" + str(publicacion.id))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        self.assertEqual(Destacada.objects.all().count(), cantidad_destacados_inicial + 1)
        cont = ContadorVida.objects.get(perfil=self.p)
        self.assertEqual(cont.numVidasSemanales, 0)

        ultima_destacada = Destacada.objects.last()
        self.assertEqual(ultima_destacada.publicacion, publicacion)

        # Intentamos volver a destacar una publicación destacada y no se crea otra vez
        response = self.client.get("/publicacion/destacar/" + str(publicacion.id))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        self.assertEqual(Destacada.objects.all().count(), cantidad_destacados_inicial + 1)

    def test_destacar_otro_usuario_logged(self):
        # Creamos nuevo usuario
        User.objects.create(username='prueba2', password='prueba2')

        cantidad_destacados_inicial = Destacada.objects.all().count()
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        self.client.post('', answers)

        # Usuario 1 realiza una publicación
        response = super().publicar(self.p, Categorias.SALON)
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

    def test_destacar_premium_logged(self):
        answers = {
            'username': 'prueba3',
            'password': 'usuario1234'
        }
        self.client.post('', answers)

        # Contamos la cantidad de publicaciones destacadas que tenemos inicialmente
        cantidad_destacados_inicial = Destacada.objects.all().count()

        Premium.objects.create(perfil=self.p2)
        response = super().publicar(self.p2, Categorias.SALON)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        # Al destacar la última publicación, confirmamos que hay una publicación destacada más y que coincide
        publicacion = Publicacion.objects.last()
        response = self.client.get("/publicacion/destacar/" + str(publicacion.id))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        self.assertEqual(Destacada.objects.all().count(), cantidad_destacados_inicial + 1)

        ultima_destacada = Destacada.objects.last()
        self.assertEqual(ultima_destacada.publicacion, publicacion)

        # Intentamos volver a destacar una publicación destacada y no se crea otra vez
        response = self.client.get("/publicacion/destacar/" + str(publicacion.id))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        self.assertEqual(Destacada.objects.all().count(), cantidad_destacados_inicial + 1)
        up = UsuarioPerfil.objects.get(user=self.u2)
        self.assertEqual(up.totalPuntos, 90)
    
    def test_mostrar_publicacion(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        self.client.post('', answers)
        response = super().publicar(self.p, Categorias.SALON)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        publicacion = Publicacion.objects.last()
        response = self.client.get('/publicacion/' + str(publicacion.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='publicacion/mostrar.html')

    def test_comentar_publicacion(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        self.client.post('', answers)
        response = super().publicar(self.p, Categorias.SALON)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')
        publicacion = Publicacion.objects.last()
        response = self.client.get('/publicacion/' + str(publicacion.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='publicacion/mostrar.html')
        answers = {
            'texto': 'Comentario de prueba',
            'publicacion_id': publicacion.id
        }
        response = self.client.post('/publicacion/comentar/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='publicacion/mostrar.html')
        self.assertEqual(Comentario.objects.all().count(), 1)
        c = Comentario.objects.last()
        self.assertEqual(c.texto, 'Comentario de prueba')