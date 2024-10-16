from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Notas

class NotasTests(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.login(username='testuser', password='testpassword123')
    
    def test_crear_nota_exitosa(self):
        """
        Creación de nota exitosa:
        Resultado esperado: La nota aparece en la lista de notas con el título y contenido correctos.
        """
        response = self.client.post(reverse('crear_nota'), {
            'titulo': 'Nueva Nota',
            'descripcion': 'Contenido de la nueva nota' 
        })
        self.assertEqual(response.status_code,302)  # Redirige después de crear la nota
        self.assertTrue(Notas.objects.filter(titulo='Nueva Nota', descripcion='Contenido de la nueva nota').exists())

    def test_crear_nota_campos_vacios(self):
        """
        Creación de nota con título y contenido vacío:
        Resultado esperado: Aparece un mensaje de error indicando que el título es obligatorio.
        """
        response = self.client.post(reverse('crear_nota'), {
            'titulo': '',
            'descripcion': ''
        })
        self.assertEqual(response.status_code, 200)  # Se queda en la misma página
        self.assertContains(response, "Completa este campo")  # Verifica si hay un mensaje de error
        self.assertFalse(Notas.objects.filter(titulo='', descripcion='').exists())

    def test_visualizar_nota_especifica(self):
        """
        Visualización de una nota específica:
        Resultado esperado: Se muestra el contenido completo de la nota seleccionada.
        """
        nota = Notas.objects.create(titulo='Nota de prueba', descripcion='Contenido de la nota', usuario=self.user)
        response = self.client.get(reverse('list_tareas'))
        self.assertContains(response, 'Nota de prueba')
        self.assertContains(response, 'Contenido de la nota')

    def test_editar_nota_exitosa(self):
        """
        Edición de una nota exitosa:
        Resultado esperado: Los cambios se guardan correctamente y la nota actualizada se muestra en la lista.
        """
        nota = Notas.objects.create(titulo='Nota original', descripcion='Descripción original', usuario=self.user)
        response = self.client.post(reverse('actualizar_nota', args=[nota.id]), {
            'titulo': 'Nota actualizada',
            'descripcion': 'Descripción actualizada'
        })
        self.assertEqual(response.status_code,302)  # Redirige después de la actualización
        nota.refresh_from_db()
        self.assertEqual(nota.titulo, 'Nota actualizada')
        self.assertEqual(nota.descripcion, 'Descripción actualizada')

    def test_eliminar_nota(self):
        """
        Eliminación de una nota:
        Resultado esperado: La nota se elimina de la lista y ya no es accesible.
        """
        nota = Notas.objects.create(titulo='Nota a eliminar', descripcion='Contenido de la nota a eliminar', usuario=self.user)
        response = self.client.post(reverse('eliminar_nota', args=[nota.id]))
        self.assertEqual(response.status_code, 302)  # Redirige después de la eliminación
        self.assertFalse(Notas.objects.filter(id=nota.id).exists())
