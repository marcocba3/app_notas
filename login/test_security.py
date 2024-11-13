from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SecurityTests(TestCase):

    def setUp(self):
        # Crear un usuario para las pruebas de seguridad
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_sql_injection(self):
        # Prueba básica para verificar si la vista es vulnerable a inyecciones SQL
        response = self.client.post(reverse('login'), {
            'username': "' OR 1=1 --",
            'password': 'testpassword123'
        })
        # Verificar que el usuario no sea autenticado con un payload de inyección SQL
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SecurityTests(TestCase):

    def setUp(self):
        # Crear un usuario para las pruebas de seguridad
        self.user = User.objects.create_user(username='testuser', password='testpassword123')



    def test_xss_protection(self):
        # Simula un ataque XSS enviando un script como nombre de usuario
        response = self.client.post(reverse('login'), {
            'username': '<script>alert("XSS")</script>',
            'password': 'testpassword123'
        })
        
        # Verificar que el contenido no contenga el script, y no sea ejecutado en la respuesta
        self.assertNotContains(response, '<script>alert("XSS")</script>')
        self.assertEqual(response.status_code, 200)

    def test_username_enumeration(self):
        # Verificar que no se pueda hacer enumeración de usuarios
        response = self.client.post(reverse('login'), {
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        })
        
        # Asegurarse de que el mensaje de error sea genérico para no revelar si el usuario existe
        self.assertContains(response, "Please enter a correct username and password.")
        self.assertNotContains(response, "The username does not exist.")
