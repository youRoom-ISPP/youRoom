from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class LoginTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba@gmail.com'
        self.u.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_login_ok(self):
        answers = {
            'username': 'prueba',
            'password1': 'usuario1234'
        }
        response = self.client.post('', answers)
        self.assertEqual(response.status_code, 200)

    
