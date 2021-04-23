from django.core.management import call_command
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida


class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.isActive = True
        self.u.save()
        self.p = UsuarioPerfil.objects.get_or_create(user=self.u, totalPuntos=100)[0]
        self.c = ContadorVida.objects.get_or_create(perfil=self.p, estaActivo=True)[0]
        call_command('loaddata', 'products.json', verbosity=0)
