from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from tienda.tests_views import TiendaViewTest
from django.contrib.auth.models import User
from usuario.models import UsuarioPerfil, ContadorVida, Premium
import time

class TiendaInterfaceTest(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        self.base = TiendaViewTest()
        self.base.setUp()

        self.base.u2 = User(username='prueba2')
        self.base.u2.set_password('usuario1234')
        self.base.u2.email = 'prueba2@gmail.com'
        self.base.u2.isActive=True
        self.base.u2.save()
        self.base.p2 = UsuarioPerfil.objects.get_or_create(user = self.base.u2,totalPuntos=100)[0]
        self.base.c2= ContadorVida.objects.get_or_create(perfil=self.base.p2,estaActivo=True)[0]

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()
        self.base.tearDown()

    def test_interface_suscription(self):
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("prueba")
        self.driver.find_element(By.ID, "password").send_keys("usuario1234")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(5) .leyenda-icono").click()
        self.driver.find_element(By.CSS_SELECTOR, ".bi-gear-fill").click()
        self.driver.find_element(By.LINK_TEXT, "Suscríbete").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "btnSus").click()
        self.driver.switch_to.frame(0)
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys("prueba@gmail.com")
        campos = self.driver.find_elements_by_xpath("//input[@type='tel']")
        campos[0].send_keys("4242 4242 4242 4242")
        campos[1].send_keys("03 / 25")
        campos[2].send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".Button-animationWrapper-child--primary").click()
        time.sleep(4)
        self.driver.switch_to.default_content()
        self.assertFalse(ContadorVida.objects.get(perfil=self.base.p).estaActivo)

    def test_interface_cancel_suscription(self):
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("prueba2")
        self.driver.find_element(By.ID, "password").send_keys("usuario1234")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(5) .leyenda-icono").click()
        self.driver.find_element(By.CSS_SELECTOR, ".bi-gear-fill").click()
        self.driver.find_element(By.LINK_TEXT, "Suscríbete").click()
        time.sleep(2)
        self.driver.find_element(By.ID, "btnSus").click()
        self.driver.switch_to.frame(0)
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys("prueba2@gmail.com")
        campos = self.driver.find_elements_by_xpath("//input[@type='tel']")
        campos[0].send_keys("4242 4242 4242 4242")
        campos[1].send_keys("03 / 25")
        campos[2].send_keys("123")
        self.driver.find_element(By.CSS_SELECTOR, ".Button-animationWrapper-child--primary").click()
        time.sleep(4)
        self.driver.switch_to.default_content()
        self.driver.find_element(By.CSS_SELECTOR, ".bi-gear-fill").click()
        self.driver.find_element(By.LINK_TEXT, "Cancelar suscripción").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "btnCancelarSus").click()
        time.sleep(3)
        self.assertIsNotNone(Premium.objects.get(perfil=self.base.p2).fechaCancelacion)




