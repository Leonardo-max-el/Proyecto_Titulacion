from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib.auth import authenticate, login , logout
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.urls import reverse  # Importar reverses


from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from app_titulacion.models import User,Estudiante
from django.contrib import messages


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



def clouses(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            if request.user.is_authenticated:
                logout(request)
            return redirect(reverse('login'))  # Usar reverse para generar la URL del login
    return redirect('index')  # Si no es POST, redirigir al índice



@never_cache
def custom_login_view(request):
    if request.method == 'GET':
        return render(request, './accesos/login.html', {
            'form': AuthenticationForm
        })

    else:
        try:
            # Print form data to see what we're receiving
            print("Form data:", request.POST)
            
            # Get username and password from form
            username = request.POST.get('username', '')  # Using get() with default value
            password = request.POST.get('password', '')
            
            # Authenticate with username (which contains DNI)
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('inicio_titulacion')
            else:
                return render(request, './accesos/login.html', {
                    'form': AuthenticationForm,
                    'error': "Usuario o contraseña incorrecta"
                })
                
        except Exception as e:
            print("Login error:", str(e))  # Add error logging
            return render(request, './accesos/login.html', {
                'form': AuthenticationForm,
                'error': "Error en el inicio de sesión. Por favor, intente nuevamente."
            })