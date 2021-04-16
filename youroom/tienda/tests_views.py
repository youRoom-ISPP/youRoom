import io, os
from PIL import Image
from django.core.management import call_command
from rest_framework.test import  APIClient , APITestCase
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida, Premium
from tienda.models import Product
from django.urls import reverse

class TiendaViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.isActive=True
        self.u.save()
        self.p = UsuarioPerfil.objects.get_or_create(user = self.u,totalPuntos=100)[0]
        self.c= ContadorVida.objects.get_or_create(perfil=self.p,estaActivo=True)[0]
        call_command('loaddata', 'products.json', verbosity=0)


    def tearDown(self):
        self.client = None

    def test_tienda_view_not_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("home")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_charge_view_not_logged(self):
        response = self.client.get('/tienda/pago/1')
        self.assertEqual(response.status_code, 301)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_tienda_view(self):
        self.client.login(username='prueba', password='usuario1234')

        response = self.client.get("http://testserver{}".format(reverse("home")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='tienda/home.html')

    def test_cancelar_premium_logged(self):

        self.client.login(username='prueba', password='usuario1234')
    
        prem = Premium.objects.get_or_create(perfil=self.p)[0]
        perfil = UsuarioPerfil.objects.get(user=self.u)
        perfil.id_stripe = 'cus_JIUr31c2MApWC6'
        perfil.save()
        self.assertIsNone(prem.fechaCancelacion)
        
        response = self.client.get("http://testserver{}".format(reverse("cancel")))
        prem = Premium.objects.get_or_create(perfil=self.p)[0]

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(prem.fechaCancelacion)
        self.assertTemplateUsed(template_name='perfil/perfil.html')



