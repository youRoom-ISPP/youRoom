import os
from django.urls import reverse
from publicacion.enum import Categorias
from publicacion.models import Publicacion
from usuario.models import Premium
from youroom.base_tests import BaseTestCase


class TimelineViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        self.client = None
        if os.path.exists('./media/publicaciones/test.png'):
            os.remove('./media/publicaciones/test.png')

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
        self.client.login(username='prueba', password='usuario1234')

        response = self.client.get('/timeline/Dormitorio')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='timeline/timeline.html')

    def test_timeline_logged(self):
        # El usuario se loguea y accede a su perfil
        self.client.login(username='prueba', password='usuario1234')

        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='timeline/timeline.html')

    def test_timeline_new_publicacion_logged(self):

        self.client.login(username='prueba', password='usuario1234')

        # El usuario entra a la Timeline y no ve ninguna publicación
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 0)

        # El usuario entra a la categoría Dormitorio y no ve ninguna publicación
        response = self.client.get('/timeline/Dormitorio')
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 0)

        # El usuario realiza una publicación de la categoría Dormitorio
        self.assertEqual(response.status_code, 200)

        response = super().publicar(self.p, Categorias.DORMITORIO)
        self.assertEqual(response.status_code, 200)

        # El usuario entra a la Timeline y encuentra una publicación
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 1)
        self.assertEqual(publicaciones[0][0].categoria, str(Categorias.DORMITORIO))

        # El usuario entra a la categoría Escritorio y no encuentra ninguna publicación
        response = self.client.get('/timeline/Escritorio')
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 0)

        # El usuario entra a la categoría Dormitorio y encuentra una publicación
        response = self.client.get('/timeline/Dormitorio')
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 1)
        self.assertEqual(publicaciones[0][0].categoria, str(Categorias.DORMITORIO))

    def test_timeline_destacar_orden_logged(self):

        self.client.login(username='prueba', password='usuario1234')

        Premium.objects.create(perfil=self.p)
        response = super().publicar(self.p, Categorias.DORMITORIO)
        self.assertEqual(response.status_code, 200)

        # El usuario entra a la Timeline y la primera imagen que ve es su publicación
        publicacion1 = Publicacion.objects.last()
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 1)
        self.assertEqual(publicaciones[0][0], publicacion1)

        # El usuario realiza una segunda publicación y le sale la primera en la timeline
        response = super().publicar(self.p, Categorias.ENTRADITA)
        self.assertEqual(response.status_code, 200)

        publicacion2 = Publicacion.objects.last()
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 2)
        self.assertEqual(publicaciones[0][0], publicacion2)
        self.assertEqual(publicaciones[1][0], publicacion1)

        # El usuario destaca la 1 publicación y ahora sale la primera
        response = self.client.get("/publicacion/destacar/" + str(publicacion1.id))
        self.assertEqual(response.status_code, 302)

        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        publicaciones = response.context['publicaciones']
        self.assertEqual(len(publicaciones), 2)
        self.assertEqual(publicaciones[0][0], publicacion1)
        self.assertEqual(publicaciones[1][0], publicacion2)
