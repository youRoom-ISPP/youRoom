import io
from PIL import Image
from django.test import TestCase
from rest_framework.test import RequestsClient
from django.urls import reverse


class PublicacionViewTest(TestCase):

    # def generate_photo_file(self):
    #     file = io.BytesIO()
    #     image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    #     image.save(file, 'png')
    #     file.name = 'test.png'
    #     file.seek(0)
    #     return file

    def test_publicacion_view(self):
        client = RequestsClient()
        response = client.get("http://testserver{}".format(reverse('publicacion')))
        self.assertEqual(response.status_code, 200)

    # def test_subir_publicacion_view(self):
    #     client = RequestsClient()
    #     formulario = client.get("http://testserver{}".format(reverse('publicacion')))
    #     csrftoken = formulario.cookies['csrftoken']
    #     imagen = self.generate_photo_file()
    #     response = client.post("http://testserver{}".format(reverse('publicacion_guardar')), {'imagen': imagen, 'csrfmiddlewaretoken': csrftoken, 'format': 'multipart/form-data'})
    #     self.assertEqual(response.status_code, 200)
