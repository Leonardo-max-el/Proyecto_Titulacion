from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app_titulacion.models import DocumentoEstudiante
from django.contrib import messages
from django.shortcuts import redirect


@login_required
def inicio_titulacion(request):
    return render(request, 'estudiante/inicio_titulacion.html')

def seleccion_modalidad(request):
    return render(request, './estudiante/seleccion_modalidad.html')

def modalidad_titulacion(request):
    return render(request, './estudiante/modalidad_titulacion.html')


@login_required
def seleccion_modalidad (request):
    return render(request,'./estudiante/seleccion_modalidad.html')


@login_required
def modalidad_1(request):
    estudiante = DocumentoEstudiante.objects.filter(
        estudiante=request.user, modalidad='modalidad_1'
    ).first()

    if request.method == 'POST':
        if not estudiante:
            estudiante = DocumentoEstudiante.objects.create(
                estudiante=request.user, modalidad='modalidad_1'
            )

        # Handle carrera field separately
        carrera = request.POST.get('carrera')
        if carrera:
            estudiante.carrera = carrera
            if estudiante.estado_carrera in ["pendiente", "corregir"]:
                estudiante.estado_carrera = 'pendiente'

        # Handle file uploads
        archivos = ['dni_1', 'tesis', 'declaracion_jurada', 'copia_bachiller_1', 'boucher_pago_1',
                     'solicitud_1']    
        for archivo in archivos:
            archivo_subido = request.FILES.get(archivo)
            if archivo_subido:
                setattr(estudiante, archivo, archivo_subido)
                estado_actual = getattr(estudiante, f"estado_{archivo}")
                if estado_actual in ["pendiente", "corregir"]:
                    setattr(estudiante, f"estado_{archivo}", 'pendiente')

        estudiante.save()
        messages.success(request, "Datos actualizados correctamente.")
        return redirect('modalidad_1')

    return render(request, 'estudiante/modalidad_1.html', {
        'archivos_enviados': estudiante is not None,
        'estudiante': estudiante  
    })



@login_required
def modalidad_2(request):
    estudiante = DocumentoEstudiante.objects.filter(
        estudiante=request.user, modalidad='modalidad_2'
    ).first()  # Busca el registro sin crearlo automáticamente

    if request.method == 'POST':
        if not estudiante:
            estudiante = DocumentoEstudiante.objects.create(
                estudiante=request.user, modalidad='modalidad_2'
            )  # Se crea solo si el usuario envía algo por primera vez


        archivos = ['carrera','dni_1','dni_2', 'tesis', 'declaracion_jurada', 'copia_bachiller_1','copia_bachiller_2', 'boucher_pago_1',
                    'boucher_pago_2',  'solicitud_1', 'solicitud_2']    
        for archivo in archivos:
            archivo_subido = request.FILES.get(archivo)
            if archivo_subido:
                setattr(estudiante, archivo, archivo_subido)

                # Solo cambiar el estado a "pendiente" si estaba en "corregir" o "pendiente"
                estado_actual = getattr(estudiante, f"estado_{archivo}")
                if estado_actual in ["pendiente", "corregir"]:
                    setattr(estudiante, f"estado_{archivo}", 'pendiente')

        estudiante.save()
        messages.success(request, "Datos actualizados correctamente.")
        return redirect('modalidad_2')

    return render(request, 'estudiante/modalidad_2.html', {
        'archivos_enviados': estudiante is not None,
        'estudiante': estudiante  
    })





# @login_required
# def modalidad_2(request):

#     archivos_enviados = DocumentoEstudiante.objects.filter(estudiante=request.user).exists()


#     if request.method == 'POST':
#         carrera = request.POST.get('carrera')
#         dni_1 = request.FILES.get('dni_1')
#         dni_2 = request.FILES.get('dni_2')
#         # pago = request.FILES.get('pago')
#         # tesis = request.FILES.get('tesis')
#         # copia_bachiller_1 = request.FILES.get('copia_bachiller_1')
#         # copia_bachiller_2 = request.FILES.get('copia_bachiller_2')
#         # declaracion_jurada = request.FILES.get('declaracion_jurada')
#         # boucher_pago_1 = request.FILES.get('boucher_pago_1')
#         # boucher_pago_2 = request.FILES.get('boucher_pago_2')

#         # solicitud_1 = request.FILES.get('solicitud_1')
#         # solicitud_2 = request.FILES.get('solicitud_2')

#         DocumentoEstudiante.objects.create(
#             carrera = carrera,
#             estudiante=request.user,
#             # declaracion_jurada=declaracion_jurada,
#             # pago=pago,
#             # tesis=tesis,
#             modalidad='modalidad_2',

#             dni_1=dni_1,
#             dni_2=dni_2,
           
#             # copia_bachiller_1=copia_bachiller_1,
#             # copia_bachiller_2=copia_bachiller_2,

#             # boucher_pago_1=boucher_pago_1,
#             # boucher_pago_2=boucher_pago_2,

#             # solicitud_1 = solicitud_1,
#             # solicitud_2 = solicitud_2,
#         )

#         # Marcar que los archivos fueron enviados
#         archivos_enviados = True


#         messages.success(request, "Datos cargados correctamente, espero la validación y aprobación del área de Grados y Títulos.")

#         return redirect('modalidad_2')
    
#     return render(request, 'estudiante/modalidad_2.html',{'archivos_enviados': archivos_enviados})
