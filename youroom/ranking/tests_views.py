from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida
from ranking.models import Valoracion
from publicacion.models import Publicacion
from publicacion.enum import Categorias
from django.urls import reverse
from youroom.base_tests import BaseTestCase


class ValorarTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_valorar(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        self.client.post('', answers)
        self.assertTemplateUsed(template_name='timeline/timeline.html')

        response = super().publicar(self.p, Categorias.SALON)

        answers = {
            'puntuacion': 4,
            'publicacion_id': Publicacion.objects.last().id
            }

        response = self.client.post('/timeline/valorar/', answers)
        self.assertEqual(response.status_code, 200)

        objeto_guardado = Valoracion.objects.last()
        self.assertEqual(objeto_guardado.usuario.user.username, 'prueba')
        self.assertEqual(objeto_guardado.publicacion.id, Publicacion.objects.last().id)
        self.assertEqual(objeto_guardado.puntuacion, 4)


class RankingTestCase(BaseTestCase):

    def setUp(self):
        self.u1 = User(username='prueba1')
        self.u1.set_password('usuario1234')
        self.u1.email = 'prueba1@gmail.com'
        self.u1.isActive = True
        self.u1.save()
        self.p1 = UsuarioPerfil.objects.get_or_create(user=self.u1)[0]
        self.p1.totalPuntos = 300
        self.p1.save()
        self.c1 = ContadorVida.objects.get_or_create(perfil=self.p1, estaActivo=True)[0]
        self.c1.save()

        self.u2 = User(username='prueba2')
        self.u2.set_password('usuario1234')
        self.u2.email = 'prueba2@gmail.com'
        self.u2.isActive = True
        self.u2.save()
        self.p2 = UsuarioPerfil.objects.get_or_create(user=self.u2)[0]
        self.p2.totalPuntos = 200
        self.p2.save()
        self.c2 = ContadorVida.objects.get_or_create(perfil=self.p2, estaActivo=True)[0]
        self.c2.save()

    def tearDown(self):
        super().tearDown()

    def test_ranking(self):
        answers = {
            'username': 'prueba1',
            'password': 'usuario1234'
        }
        self.client.post('', answers)
        self.assertTemplateUsed(template_name='timeline/timeline.html')

        response = self.client.get("http://testserver{}".format(reverse("ranking")))
        self.assertEqual(response.status_code, 200)

        lista_usuarios = response.context['usuarios']
        self.assertEqual(len(lista_usuarios), 2)
        self.assertEqual(lista_usuarios[0], self.p1)
        self.assertEqual(lista_usuarios[1], self.p2)
