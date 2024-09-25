from django.urls import path
from .views import list_tareas, crear_nota, eliminar_nota, actualizar_nota

urlpatterns = [
    path('', list_tareas, name='list_tareas'),  # Listar notas
    path('notas/agregar/', crear_nota, name='crear_nota'),  # Agregar una nueva nota
    path('notas/eliminar/<int:nota_id>/', eliminar_nota, name='eliminar_nota'),
    path('notas/actualizar/<int:nota_id>/', actualizar_nota, name='actualizar_nota'),
]
