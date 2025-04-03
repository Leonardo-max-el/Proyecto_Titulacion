from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app_titulacion.models import Docente, Expediente, Mensaje, Documento
from django.contrib import messages
from django.utils import timezone

@login_required
def inicio_docente(request):
    try:
        docente = Docente.objects.get(user=request.user)
        expedientes_count = Expediente.objects.filter(asesor=docente).count()
        return render(request, 'docente/inicio_docente.html', {
            'docente': docente,
            'expedientes_count': expedientes_count
        })
    except Docente.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de docente.')
        return redirect('login')

@login_required
def lista_expedientes(request):
    try:
        docente = Docente.objects.get(user=request.user)
        expedientes_asignados = Expediente.objects.filter(asesor=docente).order_by('-fecha_actualizacion')
        
        if request.method == 'POST':
            expediente_id = request.POST.get('expediente_id')
            mensaje = request.POST.get('mensaje')
            expediente = get_object_or_404(Expediente, id=expediente_id)
            
            # Crear mensaje
            if mensaje:
                nuevo_mensaje = Mensaje.objects.create(
                    expediente=expediente,
                    remitente=request.user,
                    destinatario=expediente.estudiante.user,
                    asunto='Respuesta del asesor',
                    contenido=mensaje,
                    tipo='respuesta'
                )
                
                # Manejar archivos adjuntos
                if 'archivos' in request.FILES:
                    for archivo in request.FILES.getlist('archivos'):
                        Documento.objects.create(
                            expediente=expediente,
                            tipo_documento='otros',
                            archivo=archivo,
                            estado='pendiente'
                        )
                
                messages.success(request, 'Respuesta enviada correctamente.')
                return redirect('lista_expedientes_docente')
        
        return render(request, 'docente/lista_expedientes_docente.html', {
            'expedientes_asignados': expedientes_asignados
        })
    except Docente.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de docente.')
        return redirect('login')
