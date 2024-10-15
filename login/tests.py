from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class LoginTests(TestCase):
    
    def setUp(self):
        # Crear un usuario para probar el inicio de sesión
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
    
    def test_login_success(self):
        """
        Inicio de sesión exitoso:
        Resultado esperado: El usuario es redirigido a la página principal.
        
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirige después del login
        self.assertRedirects(response, '/notas/')  # Redirige a la página principal o alguna vista específica
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        """
        Inicio de sesión con credenciales incorrectas:
        Resultado esperado: Se muestra un mensaje de error "Credenciales incorrectas" y no se permite el acceso.
        
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # No redirige, se mantiene en la misma página
        self.assertContains(response, "Please enter a correct username and password.")  # Si este mensaje está en la plantilla
        self.assertFalse(response.wsgi_request.user.is_authenticated)


    def test_login_empty_fields(self):
        """
        Inicio de sesión con campos vacíos:
        Resultado esperado: Aparece un mensaje de error indicando que ambos campos son obligatorios.
        """
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)  # No redirige, se queda en la página de login
        self.assertContains(response, "This field is required.")  # Verifica si hay mensajes de error
        self.assertFalse(response.wsgi_request.user.is_authenticated)
