import io, os
from PIL import Image
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
        self.u2 = User(username='prueba3')
        self.u2.set_password('usuario1234')
        self.u2.email = 'prueba3@gmail.com'
        self.u2.isActive=True
        self.u2.save()
        self.p2 = UsuarioPerfil.objects.get_or_create(user = self.u2,totalPuntos=100,id_stripe="cus_JIUr31c2MApWC6")[0]
        self.c2= ContadorVida.objects.get_or_create(perfil=self.p2,estaActivo=True)[0]
        self.suscripcion = Product.objects.get_or_create(id=1,price="399",numVidas=0)[0]


    def tearDown(self):
        self.client = None

    def test_tienda_view_not_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("tienda")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_tienda_view(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        login = self.client.post('', answers)
        response = self.client.get("http://testserver{}".format(reverse("tienda")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='tienda/tienda.html')

    def test_cancelar_premium_logged(self):

        answers = {
            'username': 'prueba3',
            'password': 'usuario1234'
        }
        login = self.client.post('', answers)

        prem = Premium.objects.get_or_create(perfil=self.p2)[0]
        fechaCancelacion = prem.fechaCancelacion

        response = self.client.get("http://testserver{}".format(reverse("cancelar")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

