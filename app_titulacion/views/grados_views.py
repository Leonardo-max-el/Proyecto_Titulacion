from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_titulacion.models import Expediente, Documento, Docente, Mensaje
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import json

@login_required
def lista_expedientes(request):
    expedientes = Expediente.objects.all().order_by('-fecha_creacion')
    return render(request, 'grados/lista_expedientes.html', {
        'expedientes': expedientes
    })

@login_required
def gestionar_expediente_admin(request, expediente_id):
    expediente = get_object_or_404(Expediente, id=expediente_id)
    
    if request.method == 'POST':
        # Manejar la asignación del asesor
        if request.POST.get('action') == 'asignar_asesor':
            asesor_id = request.POST.get('asesor_id')
            mensaje_contenido = request.POST.get('mensaje')
            if asesor_id:
                asesor = get_object_or_404(Docente, id=asesor_id)
                expediente.asesor = asesor
                expediente.save()
                
                # Crear mensaje de asignación
                from app_titulacion.models import Mensaje
                Mensaje.objects.create(
                    expediente=expediente,
                    remitente=request.user,
                    destinatario=asesor.user,
                    asunto=f'Asignación de Asesor - {expediente.get_modalidad_display()}',
                    contenido=mensaje_contenido,
                    tipo='asignacion'
                )
                
                messages.success(request, 'Asesor asignado correctamente')
            else:
                expediente.asesor = None
                expediente.save()
                messages.success(request, 'Asesor removido correctamente')
            return redirect('gestionar_expediente_admin', expediente_id=expediente_id)

        # Actualizar estado del expediente solo si se proporciona un nuevo estado
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado:
            expediente.estado = nuevo_estado
            expediente.save()
            messages.success(request, 'Estado del expediente actualizado correctamente')
        
        # Actualizar estado de documentos individuales
        for documento in expediente.documentos.all():
            estado = request.POST.get(f'estado_{documento.id}')
            if estado:
                documento.estado = estado
                documento.save()
        
        return redirect('gestionar_expediente_admin', expediente_id=expediente_id)
    
    docentes = Docente.objects.all()
    return render(request, 'grados/gestionar_expediente_admin.html', {
        'expediente': expediente,
        'docentes': docentes
    })

@login_required
def actualizar_observaciones(request, documento_id):
    if request.method == 'POST':
        try:
            documento = get_object_or_404(Documento, id=documento_id)
            data = request.POST.get('observaciones')
            action = request.POST.get('action', 'update')  # Por defecto es 'update'
            
            if action == 'delete':
                documento.observaciones = None
                documento.estado = 'pendiente'  # Volver a pendiente al eliminar observaciones
                documento.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Observaciones eliminadas correctamente'
                })
            
            if data:
                documento.observaciones = data
                documento.estado = 'observado'
                documento.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Observaciones actualizadas correctamente'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No se proporcionaron observaciones'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)

@login_required
def actualizar_estado_documento(request, documento_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            documento = get_object_or_404(Documento, id=documento_id)
            nuevo_estado = data.get('estado')
            
            # Si el documento específico está siendo aprobado
            if nuevo_estado == 'aprobado':
                documento.estado = nuevo_estado
                documento.observaciones = None  # Establecer explícitamente como NULL en la base de datos
                documento.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Estado actualizado y observaciones eliminadas para el documento {documento_id}'
                })
            else:
                # Para otros estados, solo actualizar el estado del documento específico
                documento.estado = nuevo_estado
                documento.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Estado actualizado para el documento {documento_id}'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })

@login_required
def responder_mensaje(request, mensaje_id):
    if request.method == 'POST':
        mensaje_original = None
        try:
            mensaje_original = get_object_or_404(Mensaje, id=mensaje_id)
            contenido_respuesta = request.POST.get('contenido')
            
            if not contenido_respuesta:
                messages.error(request, 'El contenido de la respuesta no puede estar vacío')
                return redirect('gestionar_expediente_admin', expediente_id=mensaje_original.expediente.id)
            
            # Crear el mensaje de respuesta
            Mensaje.objects.create(
                expediente=mensaje_original.expediente,
                remitente=request.user,
                destinatario=mensaje_original.remitente,
                asunto=f'RE: {mensaje_original.asunto}',
                contenido=contenido_respuesta,
                tipo='respuesta',
                mensaje_padre=mensaje_original
            )
            
            messages.success(request, 'Respuesta enviada correctamente')
            return redirect('gestionar_expediente_admin', expediente_id=mensaje_original.expediente.id)
            
        except Exception as e:
            messages.error(request, f'Error al enviar la respuesta: {str(e)}')
            if mensaje_original:
                return redirect('gestionar_expediente_admin', expediente_id=mensaje_original.expediente.id)
            return redirect('lista_expedientes')
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)
