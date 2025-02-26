from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
from django.contrib.auth.models import User, Permission, Group
from django.db import IntegrityError
from django.views.decorators.cache import never_cache
from django.urls import reverse  # Importar reverse
from django.contrib.auth.decorators import login_required
from .models import DocumentoEstudiante
# Create your views here.

TEMPLATE_DIRS =(
    'os.path.join(BASE_DIR, "templates")'
)


def index(request):
    return render(request,'index.html')

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
                return redirect('./estudiante/seleccion_modalidad.html')  # O la ruta que desees para "totaladmin"

            # Si no es "totaladmin", redirigir a /list_user
            return redirect('/seleccion_modalidad')
        



@login_required
def seleccion_modalidad (request):
    return render(request,'./estudiante/seleccion_modalidad.html')


@login_required
def modalidad_1(request):
    if request.method == 'POST':
        dni = request.FILES.get('dni')
        pago = request.FILES.get('pago')
        tesis = request.FILES.get('tesis')
        copia_bachiller_1 = request.FILES.get('copia_bachiller_1')
        declaracion_jurada = request.FILES.get('declaracion_jurada')
        boucher_pago_1 = request.FILES.get('boucher_pago_1')
        
        DocumentoEstudiante.objects.create(
            estudiante=request.user,
            modalidad='modalidad_1',
            dni=dni,
            pago=pago,
            tesis=tesis,
            copia_bachiller_1=copia_bachiller_1,
            declaracion_jurada=declaracion_jurada,
            boucher_pago_1=boucher_pago_1,
        )
        return redirect('modalidad_1')
    
    return render(request, 'estudiante/modalidad_1.html')


@login_required
def modalidad_2(request):
    if request.method == 'POST':
        dni = request.FILES.get('dni')
        pago = request.FILES.get('pago')
        tesis = request.FILES.get('tesis')
        copia_bachiller_1 = request.FILES.get('copia_bachiller_1')
        copia_bachiller_2 = request.FILES.get('copia_bachiller_2')
        boucher_pago_1 = request.FILES.get('boucher_pago_1')
        boucher_pago_2 = request.FILES.get('boucher_pago_2')
        
        DocumentoEstudiante.objects.create(
            estudiante=request.user,
            modalidad='modalidad_2',
            dni=dni,
            pago=pago,
            tesis=tesis,
            copia_bachiller_1=copia_bachiller_1,
            copia_bachiller_2=copia_bachiller_2,
            boucher_pago_1=boucher_pago_1,
            boucher_pago_2=boucher_pago_2
        )
        return redirect('modalidad_2')
    
    return render(request, 'estudiante/modalidad_2.html')
