from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login , logout
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.urls import reverse  # Importar reverse


def register(request):
    
    if request.method == 'GET':    
        return render(request, './accesos/register.html', {
            'form':UserCreationForm
        })
    
    else:
        
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(first_name=request.POST["first_name"],
                                                email=request.POST["email"],
                                                password=request.POST["password1"],
                                                username=request.POST["username"]
                                                )
                user.save()
                
                user = authenticate(
                    request,
                        first_name=request.POST["first_name"],
                        email=request.POST["email"],
                        password=request.POST["password1"],
                        username=request.POST["username"]
                )
                
                if user is not None:
                    login(request, user)  # Esto ya incluye el backend correcto
                    return redirect('index')

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
        # Autenticar al usuario
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )

        if user is None:
            # Si la autenticación falla, mostrar error
            return render(request, './accesos/login.html', {
                'form': AuthenticationForm,
                'error': "La contraseña de la usuari@ es incorrecta"
            })
        else:
            # Si la autenticación es exitosa, iniciar sesión
            login(request, user)

            # Verificar si el usuario es "totaladmin"
            if user.username == "totaladmin":
                # Redirigir a una página especial si es "totaladmin"
                return redirect('seleccion_modalidad.html')  # O la ruta que desees para "totaladmin"

            # Si no es "totaladmin", redirigir a /list_user
            return redirect('seleccion_modalidad')
