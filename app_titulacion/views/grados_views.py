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

    # Obtener la modalidad desde la base de datos
    modalidad = estudiante.modalidad

    if request.method == 'POST':
        print(request.POST)
        nuevo_estado_carrera = request.POST.get('estado_carrera')

        nuevo_estado_dni_1 = request.POST.get('estado_dni_1')
        nuevo_archivo_dni_1 = request.FILES.get('dni_1')

        nuevo_estado_dni_2 = request.POST.get('estado_dni_2')
        nuevo_archivo_dni_2 = request.FILES.get('dni_2')

        nuevo_estado_tesis = request.POST.get('estado_tesis')
        nuevo_archivo_tesis = request.FILES.get('tesis')
        nuevo_estado_declaracion = request.POST.get('estado_declaracion_jurada')
        nuevo_archivo_declaracion = request.FILES.get('declaracion_jurada')
        nuevo_estado_copia_bachiller_1 = request.POST.get('estado_copia_bachiller_1')
        nuevo_archivo_copia_bachiller_1 = request.FILES.get('copia_bachiller_1')
        nuevo_estado_copia_bachiller_2 = request.POST.get('estado_copia_bachiller_2')
        nuevo_archivo_copia_bachiller_2 = request.FILES.get('copia_bachiller_2')
        nuevo_estado_boucher_1 = request.POST.get('estado_boucher_pago_1')
        nuevo_archivo_boucher_1 = request.FILES.get('boucher_pago_1')
        nuevo_estado_boucher_2 = request.POST.get('estado_boucher_pago_2')
        nuevo_archivo_boucher_2 = request.FILES.get('boucher_pago_2')
        nuevo_estado_solicitud_1 = request.POST.get('estado_solicitud_1')
        nuevo_archivo_solicitud_1 = request.FILES.get('solicitud_1')
        nuevo_estado_solicitud_2 = request.POST.get('estado_solicitud_2')
        nuevo_archivo_solicitud_2 = request.FILES.get('solicitud_2')

        # Guardar cambios de estado
        if nuevo_estado_carrera:
            estudiante.estado_carrera = nuevo_estado_carrera

        if nuevo_estado_dni_1:
            estudiante.estado_dni_1 = nuevo_estado_dni_1

        if nuevo_estado_dni_2:
            estudiante.estado_dni_2 = nuevo_estado_dni_2

        if nuevo_estado_tesis:
            estudiante.estado_tesis = nuevo_estado_tesis

        if nuevo_estado_declaracion:
            estudiante.estado_declaracion_jurada = nuevo_estado_declaracion

        if nuevo_estado_copia_bachiller_1:
            estudiante.estado_copia_bachiller_1 = nuevo_estado_copia_bachiller_1

        if nuevo_estado_copia_bachiller_2:
            estudiante.estado_copia_bachiller_2 = nuevo_estado_copia_bachiller_2

        if nuevo_estado_boucher_1:
            estudiante.estado_boucher_pago_1 = nuevo_estado_boucher_1

        if nuevo_estado_boucher_2:
            estudiante.estado_boucher_pago_2 = nuevo_estado_boucher_2

        if nuevo_estado_solicitud_1:
            estudiante.estado_solicitud_1 = nuevo_estado_solicitud_1

        if nuevo_estado_solicitud_2:
            estudiante.estado_solicitud_2 = nuevo_estado_solicitud_2

        # ✅ Manejo de archivos subidos
        archivos = [
            ('dni_2', nuevo_archivo_dni_1),
            ('dni_1', nuevo_archivo_dni_2),
            ('tesis', nuevo_archivo_tesis),
            ('declaracion_jurada', nuevo_archivo_declaracion),
            ('copia_bachiller_1', nuevo_archivo_copia_bachiller_1),
            ('copia_bachiller_2', nuevo_archivo_copia_bachiller_2),
            ('boucher_pago_1', nuevo_archivo_boucher_1),
            ('boucher_pago_2', nuevo_archivo_boucher_2),
            ('solicitud_1', nuevo_archivo_solicitud_1),
            ('solicitud_2', nuevo_archivo_solicitud_2),
        ]

        for campo, archivo in archivos:
            if archivo:
                archivo_actual = getattr(estudiante, campo)
                if archivo_actual:
                    archivo_actual.delete(save=False)  # Elimina el archivo anterior
                setattr(estudiante, campo, archivo)  # Asigna el nuevo archivo

        estudiante.save()
        messages.success(request, "Estados actualizados correctamente.")

    # ✅ Definir `contexto` siempre, incluso si no es una solicitud POST
    contexto = {
        'estudiante': estudiante,
        'modalidad': modalidad,
        'dni_1_url': estudiante.dni_1.url if estudiante.dni_1 else None
    }

    return render(request, 'grados/validar_documentos.html', contexto)
