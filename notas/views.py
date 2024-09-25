from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notas

@login_required
def list_tareas(request):
    notas = Notas.objects.filter(usuario=request.user)  # Mostrar solo las notas del usuario autenticado
    return render(request, 'lista_tareas.html', {"notas": notas})

@login_required
def crear_nota(request):
    if request.method == 'POST':
        notas = Notas(titulo=request.POST['titulo'], descripcion=request.POST['descripcion'], usuario=request.user)  # Asociar la nota al usuario autenticado
        notas.save()
        return redirect('list_tareas')
    return render(request, 'agregar_nota.html')

@login_required
def eliminar_nota(request, nota_id):
    nota = get_object_or_404(Notas, id=nota_id, usuario=request.user)  # Asegurarse de que la nota pertenezca al usuario autenticado
    nota.delete()
    return redirect('list_tareas')

@login_required
def actualizar_nota(request, nota_id):
    nota = get_object_or_404(Notas, id=nota_id, usuario=request.user)  # Solo permitir al usuario propietario de la nota
    if request.method == 'POST':
        nota.titulo = request.POST['titulo']
        nota.descripcion = request.POST['descripcion']
        nota.save()
        return redirect('list_tareas')
    return render(request, 'actualizar_nota.html', {'nota': nota})