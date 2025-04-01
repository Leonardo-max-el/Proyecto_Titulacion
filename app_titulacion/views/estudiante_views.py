from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app_titulacion.models import Expediente, Documento, Estudiante
from django.contrib import messages
import os

@login_required
def inicio_titulacion(request):
    # Obtener el estudiante asociado al usuario actual
    estudiante = Estudiante.objects.get(user=request.user)
    # Obtener todos los expedientes del estudiante
    expedientes = Expediente.objects.filter(estudiante=estudiante)
    
    return render(request, 'estudiante/inicio_titulacion.html', {
        'expedientes': expedientes
    })

@login_required
def crear_expediente(request):
    if request.method == 'POST':
        try:
            estudiante = Estudiante.objects.get(user=request.user)
            modalidad = request.POST.get('modalidad')
            
            if not modalidad:
                messages.error(request, 'Por favor seleccione una modalidad')
                return redirect('crear_expediente')
            
            expediente = Expediente.objects.create(
                estudiante=estudiante,
                modalidad=modalidad
            )
            
            messages.success(request, f'Expediente {expediente.codigo_expediente} creado exitosamente')
            return redirect('gestionar_expediente', expediente_id=expediente.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear el expediente: {str(e)}')
            return redirect('crear_expediente')
    
    return render(request, 'estudiante/crear_expediente.html', {
        'modalidades': Expediente.MODALIDAD_CHOICES
    })

@login_required
def gestionar_expediente(request, expediente_id):
    try:
        estudiante = Estudiante.objects.get(user=request.user)
        expediente = get_object_or_404(Expediente, id=expediente_id, estudiante=estudiante)
        documentos = expediente.documentos.all().order_by('-fecha_subida')

        if request.method == 'POST':
            # Verificar si el expediente está aprobado
            if expediente.estado == 'aprobado':
                messages.error(request, 'No se pueden realizar modificaciones en un expediente aprobado.')
                return redirect('gestionar_expediente', expediente_id=expediente_id)

            # Manejar eliminación de documento
            if 'action' in request.POST and request.POST['action'] == 'delete':
                documento_id = request.POST.get('documento_id')
                if documento_id:
                    documento = get_object_or_404(Documento, id=documento_id, expediente=expediente)
                    documento.delete()
                    messages.success(request, 'Documento eliminado correctamente.')
                    return redirect('gestionar_expediente', expediente_id=expediente_id)

            # Manejar actualización de documento
            if 'documento_id' in request.POST and 'archivo' in request.FILES:
                documento_id = request.POST.get('documento_id')
                if documento_id:
                    documento = get_object_or_404(Documento, id=documento_id, expediente=expediente)
                    documento.archivo = request.FILES['archivo']
                    documento.version += 1
                    documento.save()
                    messages.success(request, 'Documento actualizado correctamente.')
                    return redirect('gestionar_expediente', expediente_id=expediente_id)

            # Manejar subida de nuevos documentos
            if 'archivos' in request.FILES:
                archivos = request.FILES.getlist('archivos')
                for archivo in archivos:
                    tipo_documento = archivo.name.split('.')[0].lower()  # Obtener el tipo de documento del nombre del archivo
                    Documento.objects.create(
                        expediente=expediente,
                        tipo_documento=tipo_documento,
                        archivo=archivo,
                        estado='pendiente'
                    )
                messages.success(request, 'Documentos subidos correctamente.')
                return redirect('gestionar_expediente', expediente_id=expediente_id)

        return render(request, 'estudiante/gestionar_expediente.html', {
            'expediente': expediente,
            'documentos': documentos
        })
    except Estudiante.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de estudiante.')
        return redirect('inicio_titulacion')

    

