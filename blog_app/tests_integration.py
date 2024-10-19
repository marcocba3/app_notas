from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notas.models import Notas  # Asegúrate de que Notas esté importado correctamente

class AppIntegrationTests(TestCase):

    def test_registro_login_crear_nota(self):
        """
        Flujo completo: Registro de usuario, login, creación de nota y verificación en la lista de notas.
        """
        # Registro de usuario
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras el registro

        # Login del usuario
        self.client.login(username='newuser', password='testpassword123')

        # Crear una nota
        response = self.client.post(reverse('crear_nota'), {
            'titulo': 'Nota integración',
            'descripcion': 'Contenido integración'
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras crear la nota
        self.assertTrue(Notas.objects.filter(titulo='Nota integración', descripcion='Contenido integración').exists())
        
        # Verificar que la nota aparece en la lista
        response = self.client.get(reverse('list_tareas'))
        self.assertContains(response, 'Nota integración')

    def test_login_editar_nota(self):
        """
        Flujo de login y edición de una nota creada.
        """
        # Crear usuario y nota
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        nota = Notas.objects.create(titulo='Nota original', descripcion='Descripción original', usuario=self.user)

        # Editar la nota
        response = self.client.post(reverse('actualizar_nota', args=[nota.id]), {
            'titulo': 'Nota editada',
            'descripcion': 'Descripción editada'
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras editar
        nota.refresh_from_db()
        self.assertEqual(nota.titulo, 'Nota editada')
        self.assertEqual(nota.descripcion, 'Descripción editada')

    def test_login_eliminar_nota(self):
        """
        Flujo de login y eliminación de una nota.
        """
        # Crear usuario y nota
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
        nota = Notas.objects.create(titulo='Nota a eliminar', descripcion='Descripción para eliminar', usuario=self.user)

        # Eliminar la nota
        response = self.client.post(reverse('eliminar_nota', args=[nota.id]))
        self.assertEqual(response.status_code, 302)  # Redirige tras eliminar
        self.assertFalse(Notas.objects.filter(id=nota.id).exists())
