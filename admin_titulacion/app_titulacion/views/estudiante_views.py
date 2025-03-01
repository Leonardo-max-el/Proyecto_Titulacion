from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_titulacion.models import DocumentoEstudiante
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def seleccion_modalidad (request):
    return render(request,'./estudiante/seleccion_modalidad.html')


@login_required
def modalidad_1(request):
    estudiante, created = DocumentoEstudiante.objects.get_or_create(
        estudiante=request.user, modalidad='modalidad_1'
    )  # Obtiene o crea el registro del estudiante

    archivos_enviados = estudiante is not None  # Verifica si ya subió documentos

    if request.method == 'POST':
        estudiante.carrera = request.POST.get('carrera')
        estudiante.estado_carrera = 'pendiente'  # Marcar la carrera como pendiente si se cambia

        # Lista de archivos a actualizar
        archivos = ['dni_1']  # Agrega más si es necesario

        for archivo in archivos:
            archivo_subido = request.FILES.get(archivo)
            if archivo_subido:
                setattr(estudiante, archivo, archivo_subido)  # Reemplaza el archivo
                setattr(estudiante, f"estado_{archivo}", 'pendiente')  # Lo vuelve a marcar como pendiente

        estudiante.save()  # Guarda los cambios en la base de datos

        messages.success(request, "Datos actualizados correctamente. Espere la validación del área de Grados y Títulos.")
        return redirect('modalidad_1')

    return render(request, 'estudiante/modalidad_1.html', {
        'archivos_enviados': archivos_enviados,
        'estudiante': estudiante  
    })

@login_required
def modalidad_2(request):

    archivos_enviados = DocumentoEstudiante.objects.filter(estudiante=request.user).exists()


    if request.method == 'POST':
        carrera = request.POST.get('carrera')
        dni_1 = request.FILES.get('dni_1')
        dni_2 = request.FILES.get('dni_2')
        # pago = request.FILES.get('pago')
        # tesis = request.FILES.get('tesis')
        # copia_bachiller_1 = request.FILES.get('copia_bachiller_1')
        # copia_bachiller_2 = request.FILES.get('copia_bachiller_2')
        # declaracion_jurada = request.FILES.get('declaracion_jurada')
        # boucher_pago_1 = request.FILES.get('boucher_pago_1')
        # boucher_pago_2 = request.FILES.get('boucher_pago_2')

        # solicitud_1 = request.FILES.get('solicitud_1')
        # solicitud_2 = request.FILES.get('solicitud_2')

        DocumentoEstudiante.objects.create(
            carrera = carrera,
            estudiante=request.user,
            # declaracion_jurada=declaracion_jurada,
            # pago=pago,
            # tesis=tesis,
            modalidad='modalidad_2',

            dni_1=dni_1,
            dni_2=dni_2,
           
            # copia_bachiller_1=copia_bachiller_1,
            # copia_bachiller_2=copia_bachiller_2,

            # boucher_pago_1=boucher_pago_1,
            # boucher_pago_2=boucher_pago_2,

            # solicitud_1 = solicitud_1,
            # solicitud_2 = solicitud_2,
        )

        # Marcar que los archivos fueron enviados
        archivos_enviados = True


        messages.success(request, "Datos cargados correctamente, espero la validación y aprobación del área de Grados y Títulos.")

        return redirect('modalidad_2')
    
    return render(request, 'estudiante/modalidad_2.html',{'archivos_enviados': archivos_enviados})
