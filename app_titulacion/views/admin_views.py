from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseForbidden
from app_titulacion.models import User, Estudiante, Docente
from django.contrib.auth.hashers import make_password
from django.db import transaction

def es_superusuario(user):
    return user.is_superuser

@login_required
@user_passes_test(es_superusuario, login_url='login')
def lista_usuarios(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    usuarios = User.objects.all().select_related('estudiante')
    return render(request, 'admin/usuarios/lista_usuarios.html', {
        'usuarios': usuarios
    })

@login_required
@user_passes_test(es_superusuario, login_url='login')
def crear_usuario(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Crear usuario base
                usuario = User.objects.create(
                    username=request.POST['dni'],  # Usamos el DNI como username
                    email=request.POST['correo_institucional'],
                    password=make_password(request.POST['password']),
                    is_staff=True,  # Por defecto, los docentes tendrán acceso al admin
                    is_active=True,
                    first_name=request.POST.get('nombres', ''),
                )
                
                # Crear perfil de docente
                Docente.objects.create(
                    user=usuario,
                    dni=request.POST['dni'],
                    apellido_paterno=request.POST['apellido_paterno'],
                    apellido_materno=request.POST['apellido_materno'],
                    telefono=request.POST['telefono'],
                    correo_institucional=request.POST['correo_institucional'],
                    codigo_doctor=request.POST['codigo_doctor'],
                    direccion=request.POST['direccion']
                )
                
                messages.success(request, 'Docente creado exitosamente')
                return redirect('lista_usuarios')
                
        except Exception as e:
            messages.error(request, f'Error al crear docente: {str(e)}')
    
    return render(request, 'admin/usuarios/crear_usuario.html')

@login_required
@user_passes_test(es_superusuario, login_url='login')
def editar_usuario(request, user_id):
    try:
        usuario = get_object_or_404(User, id=user_id)
        docente = get_object_or_404(Docente, user=usuario)  # Obtener el docente relacionado
        
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    # Actualizar datos básicos del usuario
                    usuario.username = request.POST['dni']  # Usamos DNI como username
                    usuario.first_name = request.POST['nombres']
                    if request.POST.get('password'):
                        usuario.password = make_password(request.POST['password'])
                    usuario.save()
                    
                    # Actualizar datos del docente
                    docente.dni = request.POST['dni']
                    docente.apellido_paterno = request.POST['apellido_paterno']
                    docente.apellido_materno = request.POST['apellido_materno']
                    docente.telefono = request.POST['telefono']
                    docente.correo_institucional = request.POST['correo_institucional']
                    docente.codigo_doctor = request.POST['codigo_doctor']
                    docente.direccion = request.POST['direccion']
                    docente.save()
                    
                    messages.success(request, 'Docente actualizado exitosamente')
                    return redirect('lista_usuarios')
            except Exception as e:
                messages.error(request, f'Error al actualizar docente: {str(e)}')
        
        return render(request, 'admin/usuarios/editar_usuario.html', {
            'usuario': usuario,
            'docente': docente
        })
        
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('lista_usuarios')
    except Docente.DoesNotExist:
        messages.error(request, 'Perfil de docente no encontrado')
        return redirect('lista_usuarios')

@login_required
@user_passes_test(es_superusuario, login_url='login')
def eliminar_usuario(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    usuario = get_object_or_404(User, id=user_id)
    
    # Determinar el tipo de usuario
    tipo_usuario = "Usuario"
    nombre_completo = usuario.username
    
    try:
        if hasattr(usuario, 'docente'):
            tipo_usuario = "Docente"
            nombre_completo = f"Dr. {usuario.docente.apellido_paterno} {usuario.docente.apellido_materno}"
        elif hasattr(usuario, 'estudiante'):
            tipo_usuario = "Estudiante"
            nombre_completo = f"{usuario.estudiante.apellido_paterno} {usuario.estudiante.apellido_materno}"
    except:
        pass

    if request.method == 'POST':
        try:
            # La eliminación en cascada se manejará automáticamente debido a las relaciones en el modelo
            usuario.delete()
            messages.success(request, f'{tipo_usuario} {nombre_completo} eliminado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar {tipo_usuario.lower()}: {str(e)}')
        return redirect('lista_usuarios')
    
    # Si es GET, mostrar página de confirmación
    return render(request, 'admin/usuarios/confirmar_eliminacion.html', {
        'usuario': usuario,
        'tipo_usuario': tipo_usuario,
        'nombre_completo': nombre_completo
    })