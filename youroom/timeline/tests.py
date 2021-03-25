from django.test import TestCase
import io, os
from PIL import Image
from rest_framework.test import  APIClient , APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from publicacion.enum import Categorias

# Create your tests here.

class TimelineViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.u = User(username='prueba')
        self.u.set_password('prueba')
        self.u.email = 'prueba@gmail.com'
        self.u.isActive=True
        self.u.save()
    
    def tearDown(self):
        self.client = None

    def test_timeline_no_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_timeline_categoria_no_logged(self):
        response = self.client.get('/timeline/0')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')


    def test_timeline_categoria_logged(self):
        # El usuario se loguea y accede a su perfil
        self.client.login(username='prueba', password='prueba')

        response = self.client.get('/timeline/0')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='timeline/timeline.html')
    

    def test_timeline_logged(self):
        # El usuario se loguea y accede a su perfil
        self.client.login(username='prueba', password='prueba')

        response = self.client.get("http://testserver{}".format(reverse("timeline")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='timeline/timeline.html')



    