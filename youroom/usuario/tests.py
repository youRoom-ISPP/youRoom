from django.contrib.auth.models import User
from youroom.base_tests import BaseTestCase


class LoginTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.u = User(username='prueba1')
        self.u.set_password('usuario1234')
        self.u.email = 'prueba1@gmail.com'
        self.u.isActive = True
        self.u.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_login_ok(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        response = self.client.post('', answers)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/timeline/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_login_fail(self):
        answers = {
                'username': 'impostor',
                'password': 'impostor1234'
            }
        response = self.client.post('', answers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[-1], 'usuario/login.html')

    def test_registro_ok(self):
        answers = {
                'username': 'usuario_ok',
                'password1': 'usuario1234',
                'password2': 'usuario1234',
                'email': 'test@test.com',
                'descripcion': 'soy de prueba'
            }
        response = self.client.post('/registro/', answers)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.last().username, 'usuario_ok')

    def test_registro_fail_password(self):
        answers = {
                'username': 'usuario_ok',
                'password1': 'usuario123',
                'password2': 'usuario1234',
                'email': 'test@test.com',
                'descripcion': 'soy de prueba'
            }
        response = self.client.post('/registro/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(User.objects.last().username, 'usuario_ok')

    def test_registro_fail_username(self):
        answers = {
                'username': 'prueba',
                'password1': 'usuario1234',
                'password2': 'usuario1234',
                'email': 'test@test.com',
                'descripcion': 'soy de prueba'
            }
        response = self.client.post('/registro/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(User.objects.last().email, 'test@test.com')

    def test_registro_fail_email(self):
        answers = {
                'username': 'usuario_ok',
                'password1': 'usuario1234',
                'password2': 'usuario1234',
                'email': 'prueba@gmail.com',
                'descripcion': 'soy de prueba'
            }
        response = self.client.post('/registro/', answers)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(User.objects.last().username, 'usuario_ok')

    def test_listar_usuarios(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        response = self.client.post('', answers)
        response = self.client.get('/usuarios/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[-1], 'usuario/usuarios.html')

    def test_mostrar_usuario(self):
        answers = {
            'username': 'prueba',
            'password': 'usuario1234'
        }
        response = self.client.post('', answers)
        response = self.client.get('/usuarios/prueba1')
        self.assertEqual(response.status_code, 301)
        self.assertTemplateUsed(template_name='usuario/usuario.html')
