from django.urls import reverse
from youroom.base_tests import BaseTestCase


class TiendaViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

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
