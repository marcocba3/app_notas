from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notas
from django.core.exceptions import ValidationError

@login_required
def list_tareas(request):
    notas = Notas.objects.filter(usuario=request.user)  # Mostrar solo las notas del usuario autenticado
    return render(request, 'lista_tareas.html', {"notas": notas})

@login_required
def crear_nota(request):
    error_message = None
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']

        # Validación de campos vacíos
        if not titulo:
            error_message = "Completa este campo"
        elif not descripcion:
            error_message = "Completa este campo"
        elif len(titulo) > 25:
            error_message = "El título no puede tener más de 25 caracteres."
        
        # Si no hay errores, se guarda la nota
        if not error_message:
            notas = Notas(titulo=titulo, descripcion=descripcion, usuario=request.user)
            notas.save()
            return redirect('list_tareas')  # Redirige si la nota se crea correctamente

    # Si hay errores, renderiza la página de nuevo sin redirigir
    return render(request, 'agregar_nota.html', {'error_message': error_message})

@login_required
def eliminar_nota(request, nota_id):
    nota = get_object_or_404(Notas, id=nota_id, usuario=request.user)  # Asegurarse de que la nota pertenezca al usuario autenticado
    nota.delete()
    return redirect('list_tareas')

@login_required
def actualizar_nota(request, nota_id):
    nota = get_object_or_404(Notas, id=nota_id, usuario=request.user)  # Solo permitir al usuario propietario de la nota
    error_message = None
    
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        
        if len(titulo) > 25:
            error_message = "El título no puede tener más de 25 caracteres."
        else:
            nota.titulo = titulo
            nota.descripcion = descripcion
            nota.save()
            return redirect('list_tareas')

    return render(request, 'actualizar_nota.html', {'nota': nota, 'error_message': error_message})

