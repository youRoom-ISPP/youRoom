import io, os
from PIL import Image
from rest_framework.test import  APIClient , APITestCase
from django.urls import reverse
from publicacion.models import Publicacion
from publicacion.enum import Categorias

class PublicacionViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
    
    def tearDown(self):
        self.client = None
        if os.path.exists('./media/publicaciones/test.png') :
            os.remove('./media/publicaciones/test.png')

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_publicacion_view(self):
        response = self.client.get("http://testserver{}".format(reverse('publicacion')))
        self.assertEqual(response.status_code, 200)

    def test_subir_publicacion_view(self):
        formulario = self.client.get("http://testserver{}".format(reverse('publicacion')))
        csrftoken = formulario.cookies['csrftoken']
        imagen = self.generate_photo_file()
        response = self.client.post("http://testserver{}".format(reverse('publicacion_guardar')), {
            'imagen': imagen,
            'descripcion' : "Prueba",
            'categoria' : Categorias.SALON, 
            'format': 'multipart/form-data'},follow = True)
        self.assertEqual(response.status_code, 200)
        objeto_guardado = Publicacion.objects.get(id = 1)
        self.assertEqual(objeto_guardado.imagen.name, "publicaciones/" + imagen.name)
        self.assertEqual(objeto_guardado.categoria,'Categorias.SALON')
        self.assertEqual(objeto_guardado.descripcion,"Prueba")
        
        


