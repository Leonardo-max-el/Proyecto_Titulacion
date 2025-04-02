from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib.auth import authenticate, login , logout
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.urls import reverse  # Importar reverses


from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from app_titulacion.models import User,Estudiante,Docente,Administrativo
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_protect



def register(request):
    if request.method == 'POST':
        try:
            # Create and save User in DB
            user = User.objects.create_user(
                username=request.POST['dni'],
                password=request.POST['password']
            )

            # Create and save Estudiante in DB
            estudiante = Estudiante.objects.create(
                user=user,
                nombres=request.POST['nombres'],
                apellido_paterno=request.POST['apellido_paterno'],
                apellido_materno=request.POST['apellido_materno'],
                escuela_profesional=request.POST['escuela_profesional'],
                telefono=request.POST['telefono'],
                direccion=request.POST['direccion'],
                email=request.POST['email']
            )
            
            messages.success(request, '¡Usuario registrado exitosamente!')
            return redirect('login')

        except IntegrityError:
            return render(request, './accesos/register.html', 
                {'error': 'El DNI o correo electrónico ya está registrado'})
    
    # Handle GET request - show the registration form
    return render(request, './accesos/register.html')



@require_POST
def clouses(request):
    if request.user.is_authenticated:
        # Obtener la sesión actual
        session_key = request.session.session_key
        # Cerrar solo la sesión actual
        logout(request)
        # Eliminar la cookie de sesión específica
        response = JsonResponse({'status': 'success'})
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
        return response
    return JsonResponse({'status': 'not_authenticated'})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@csrf_protect
@never_cache
def custom_login_view(request):
    if request.method == 'GET':
        return render(request, './accesos/login.html', {
            'form': AuthenticationForm
        })
    else:
        try:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
                # Redirigir según el tipo de usuario
                if user.is_superuser:
                    messages.success(request, f'Bienvenido, Administrador {user.username}')
                    return redirect('lista_usuarios')
                else:
                    # Verificar el tipo de usuario
                    try:
                        docente = Docente.objects.get(user=user)
                        messages.success(request, f'Bienvenido, Dr. {docente.apellido_paterno}')
                        return redirect('inicio_docente')
                    except Docente.DoesNotExist:
                        try:
                            administrativo = Administrativo.objects.get(user=user)
                            messages.success(request, f'Bienvenido, {administrativo.nombre_completo}')
                            return redirect('lista_expedientes')
                        except Administrativo.DoesNotExist:
                            try:
                                estudiante = Estudiante.objects.get(user=user)
                                messages.success(request, f'Bienvenido, {estudiante.nombre_completo}')
                                return redirect('inicio_titulacion')
                            except Estudiante.DoesNotExist:
                                messages.error(request, "Perfil de usuario no encontrado")
                                return redirect('login')
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
                return redirect('login')
        except Exception as e:
            messages.error(request, f"Error en el inicio de sesión: {str(e)}")
            return redirect('login')

def requiere_administrativo(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser or hasattr(request.user, 'administrativo'):
            return function(request, *args, **kwargs)
        messages.error(request, 'No tienes permiso para acceder a esta página')
        return redirect('login')
    return wrap

def requiere_docente(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser or hasattr(request.user, 'docente'):
            return function(request, *args, **kwargs)
        messages.error(request, 'No tienes permiso para acceder a esta página')
        return redirect('login')
    return wrap

def requiere_estudiante(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'estudiante'):
            return function(request, *args, **kwargs)
        messages.error(request, 'No tienes permiso para acceder a esta página')
        return redirect('login')
    return wrap

class SessionManagementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Limpiar sesiones expiradas
            Session.objects.filter(expire_date__lt=timezone.now()).delete()
            
            # Obtener la sesión actual
            current_session_key = request.session.session_key
            
            # Verificar si el usuario tiene otras sesiones activas
            user_sessions = Session.objects.filter(
                expire_date__gt=timezone.now()
            ).values_list('session_key', flat=True)

            for session_key in user_sessions:
                if session_key != current_session_key:
                    # Mantener la sesión activa pero actualizar su estado
                    session = Session.objects.get(session_key=session_key)
                    if session.get_decoded().get('_auth_user_id') == str(request.user.id):
                        session.save()  # Actualizar la fecha de expiración

        response = self.get_response(request)
        return response