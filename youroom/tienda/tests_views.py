import io, os
from PIL import Image
from django.core.management import call_command
from rest_framework.test import  APIClient , APITestCase
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida, Premium
from tienda.models import Product
from django.urls import reverse
from tienda.tests import BaseTestCase

class TiendaViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()


    def tearDown(self):
        self.client = None

    def test_tienda_view_not_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("tienda")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_charge_view_not_logged(self):
        response = self.client.get('/tienda/pago/1')
        self.assertEqual(response.status_code, 301)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_tienda_view(self):
        self.client.login(username='prueba', password='usuario1234')

        response = self.client.get("http://testserver{}".format(reverse("tienda")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='tienda/tienda.html')
