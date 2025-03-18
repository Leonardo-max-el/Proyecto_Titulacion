from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login , logout
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.urls import reverse  # Importar reverses


def register(request):
    
    if request.method == 'GET':    
        return render(request, './accesos/register.html', {
            'form':UserCreationForm
        })
    
    else:
        
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST["email"],  # Using email as username
                    first_name=request.POST["first_name"],
                    email=request.POST["email"],
                    password=request.POST["password1"]
                )
                
                user.save()
                
                user = authenticate(
                    request,
                    username=request.POST["email"],  # Using email for authentication
                    password=request.POST["password1"]
                )
                
                if user is not None:
                    login(request, user)  # Esto ya incluye el backend correcto
                    return redirect('login')

            except IntegrityError:
                
                return render(request, './accesos/register.html', {'form':UserCreationForm,"error": 'EL usuario ya existe'})

        return render(request, './accesos/register.html',{'form': UserCreationForm,"error": 'Contraseñas Incorrecta'})
    

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
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            # Get the first user with this email
            user = User.objects.filter(email=email).first()
            
            if user is None:
                return render(request, './accesos/login.html', {
                    'form': AuthenticationForm,
                    'error': "El correo electrónico no está registrado"
                })

            # Authenticate using username (email) and password
            user = authenticate(
                request,
                username=user.username,  # Use the actual username from the user object
                password=password
            )

            if user is not None:
                login(request, user)
                
                if user.email == "totaladmin":
                    return redirect('inicio_titulacion')
                
                return redirect('inicio_titulacion')
            else:
                return render(request, './accesos/login.html', {
                    'form': AuthenticationForm,
                    'error': "Contraseña incorrecta"
                })
                
        except Exception as e:
            return render(request, './accesos/login.html', {
                'form': AuthenticationForm,
                'error': "Error en el inicio de sesión. Por favor, intente nuevamente."
            })