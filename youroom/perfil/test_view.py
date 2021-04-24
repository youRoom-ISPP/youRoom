import io, os
from PIL import Image
from rest_framework.test import  APIClient , APITestCase
from django.urls import reverse
from usuario.models import UsuarioPerfil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from usuario.models import UsuarioPerfil, ContadorVida
from publicacion.enum import Categorias
from tienda.models import Product
from youroom.base_tests import BaseTestCase


class PerfilViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_perfil_no_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("perfil")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_perfil_logged(self):

        # El usuario se loguea y accede a su perfil
        self.client.login(username='prueba', password='usuario1234')

        response = self.client.get("http://testserver{}".format(reverse("perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        # Su perfil es el indicado y no tiene publicaciones hechas
        perfil = response.context['user']
        publicaciones = response.context['publicaciones']

        self.assertEqual(perfil.user, self.u)
        self.assertEqual(len(publicaciones), 0)

        # El usuario realiza publicación, y al acceder a su perfil obtiene la publicación
        self.assertEqual(response.status_code, 200)

        response = super().publicar(self.p, Categorias.SALON)

        self.assertEqual(response.status_code, 200)

        response = self.client.get("http://testserver{}".format(reverse("perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        perfil = response.context['user']
        publicaciones = response.context['publicaciones']

        self.assertEqual(perfil.user, self.u)
        self.assertEqual(len(publicaciones), 1)
        self.assertEqual(publicaciones[0].usuario, perfil)

    def test_editar_perfil_no_logged(self):
        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(template_name='usuario/login.html')

    def test_editar_perfil_description_solo(self):
        
        # Comprobamos cual es la descripción inicial del usuario
        self.client.login(username='prueba', password='usuario1234')
        perfil = UsuarioPerfil.objects.get(user=self.u)
        nueva_descripcion = 'Esta es una nueva descripcion'
        password = self.u.password
        imagen = perfil.foto_perfil

        self.assertNotEqual(perfil.descripcion, nueva_descripcion)

        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        formulario = {
            'descripcion':nueva_descripcion,
            'password1':password,
            'password2':password      
        }

        response2 = self.client.post("http://testserver{}".format(reverse("guardar_perfil")), formulario)
        self.assertEqual(response2.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        perfil = UsuarioPerfil.objects.get(user=self.u)
        self.assertEqual(perfil.descripcion, nueva_descripcion)
        self.assertEqual(perfil.foto_perfil, imagen)
        self.assertTrue(perfil.user.check_password(password))

    def test_editar_perfil_password_solo(self):
        
        # Comprobamos cual es la descripción inicial del usuario
        self.client.login(username='prueba', password='usuario1234')
        perfil = UsuarioPerfil.objects.get(user=self.u)
        password = self.u.password
        descripcion_inicial = perfil.descripcion
        imagen = perfil.foto_perfil
        nueva_password = 'prueba-nueva-pass-2021'

        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        formulario = {
            'descripcion':descripcion_inicial,
            'password1':nueva_password,
            'password2':nueva_password
        }

        response2 = self.client.post("http://testserver{}".format(reverse("guardar_perfil")), formulario)
        self.assertEqual(response2.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        perfil = UsuarioPerfil.objects.get(user=self.u)
        self.assertEqual(perfil.descripcion, descripcion_inicial)
        self.assertEqual(perfil.foto_perfil, imagen)
        self.assertTrue(perfil.user.check_password(nueva_password))

    def test_editar_perfil_imagen_solo(self):
        
        # Comprobamos cual es la descripción inicial del usuario
        self.client.login(username='prueba', password='usuario1234')
        perfil = UsuarioPerfil.objects.get(user=self.u)
        descripcion = perfil.descripcion
        password = self.u.password
        imagen_inicial = perfil.foto_perfil
        imagen_nueva = self.generate_photo_file()

        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        formulario = {
            'imagen':imagen_nueva,
            'descripcion':descripcion,
            'password1':password,
            'password2':password      
        }

        response2 = self.client.post("http://testserver{}".format(reverse("guardar_perfil")), formulario)
        self.assertEqual(response2.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        perfil = UsuarioPerfil.objects.get(user=self.u)
        self.assertEqual(perfil.descripcion, descripcion)
        self.assertNotEqual(perfil.foto_perfil, imagen_inicial)
        self.assertTrue(perfil.user.check_password(password))

    def test_editar_perfil_todo(self):
        
        # Comprobamos cual es la descripción inicial del usuario
        self.client.login(username='prueba', password='usuario1234')
        perfil = UsuarioPerfil.objects.get(user=self.u)
        descripcion = perfil.descripcion
        password = self.u.password
        imagen_inicial = perfil.foto_perfil
        imagen_nueva = self.generate_photo_file()
        nueva_descripcion = 'Esta es una nueva descripcion'
        nueva_password = 'nueva_password_prueba'

        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        formulario = {
            'imagen':imagen_nueva,
            'descripcion':nueva_descripcion,
            'password1':nueva_password,
            'password2':nueva_password      
        }

        response2 = self.client.post("http://testserver{}".format(reverse("guardar_perfil")), formulario)
        self.assertEqual(response2.status_code, 302)
        self.assertTemplateUsed(template_name='perfil/perfil.html')

        perfil = UsuarioPerfil.objects.get(user=self.u)
        self.assertEqual(perfil.descripcion, nueva_descripcion)
        self.assertNotEqual(perfil.foto_perfil, imagen_inicial)
        self.assertTrue(perfil.user.check_password(nueva_password))

    def test_editar_perfil_password_diferentes(self):
        
        # Comprobamos cual es la descripción inicial del usuario
        self.client.login(username='prueba', password='usuario1234')
        perfil = UsuarioPerfil.objects.get(user=self.u)
        pass_inicial = perfil.user.password
        nueva_pass_1 = 'nueva_pas_1'
        nueva_pass_2 = 'nueva_pas_2'

        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        formulario = {
            'password1':nueva_pass_1,
            'password2':nueva_pass_2      
        }

        response2 = self.client.post("http://testserver{}".format(reverse("guardar_perfil")), formulario)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        perfil = UsuarioPerfil.objects.get(user=self.u)
        self.assertEqual(pass_inicial, perfil.user.password)

    def test_editar_perfil_password1_falta(self):
        
        # Comprobamos cual es la descripción inicial del usuario
        self.client.login(username='prueba', password='usuario1234')
        perfil = UsuarioPerfil.objects.get(user=self.u)
        pass_inicial = perfil.user.password
        nueva_pass_2 = 'nueva_pas_2'

        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        formulario = {
            'password2':nueva_pass_2,
        }

        response2 = self.client.post("http://testserver{}".format(reverse("guardar_perfil")), formulario)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        perfil = UsuarioPerfil.objects.get(user=self.u)
        self.assertEqual(pass_inicial, perfil.user.password)

    def test_editar_perfil_password2_falta(self):
        
        # Comprobamos cual es la descripción inicial del usuario
        self.client.login(username='prueba', password='usuario1234')
        perfil = UsuarioPerfil.objects.get(user=self.u)
        pass_inicial = perfil.user.password
        nueva_pass_1 = 'nueva_pas_1'

        response = self.client.get("http://testserver{}".format(reverse("editar_perfil")))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        formulario = {
            'password1':nueva_pass_1,
        }

        response2 = self.client.post("http://testserver{}".format(reverse("guardar_perfil")), formulario)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(template_name='perfil/editar_perfil.html')

        perfil = UsuarioPerfil.objects.get(user=self.u)
        self.assertEqual(pass_inicial, perfil.user.password)
        