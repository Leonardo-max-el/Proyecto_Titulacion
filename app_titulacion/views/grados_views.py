from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_titulacion.models import Expediente, Documento
from django.http import JsonResponse
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
    
    return render(request, 'grados/gestionar_expediente_admin.html', {
        'expediente': expediente
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
