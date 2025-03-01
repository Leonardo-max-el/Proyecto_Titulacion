from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app_titulacion.models import estudiante_directory_path,DocumentoEstudiante  
from django.contrib import messages


@login_required
def lista_estudiantes(request):
    estudiantes = DocumentoEstudiante.objects.all()
    return render(request, 'grados/lista_estudiantes.html', {'estudiantes': estudiantes})

@login_required
def validar_documentos(request, estudiante_id):
    estudiante = get_object_or_404(DocumentoEstudiante, id=estudiante_id)

    if request.method == 'POST':
        nuevo_estado_dni = request.POST.get('estado_dni_1')  # 🛠 Obtenemos el estado del DNI
        nuevo_estado_carrera = request.POST.get('estado_carrera')  # 🛠 Obtenemos el estado de la carrera
        nuevo_archivo_dni = request.FILES.get('dni_1')  # Obtenemos el nuevo archivo si lo suben

        # Si los valores no son None, actualizamos los campos correspondientes
        if nuevo_estado_dni:
            estudiante.estado_dni_1 = nuevo_estado_dni  

        if nuevo_estado_carrera:
            estudiante.estado_carrera = nuevo_estado_carrera  

        if nuevo_archivo_dni:
            # Eliminamos el archivo anterior antes de reemplazarlo
            if estudiante.dni_1:
                estudiante.dni_1.delete(save=False)
            estudiante.dni_1 = nuevo_archivo_dni  # Reemplazamos el archivo

        estudiante.save()  # Guardamos los cambios en la BD
        messages.success(request, "Estados actualizados correctamente.")

    return render(request, 'grados/validar_documentos.html', {'estudiante': estudiante})