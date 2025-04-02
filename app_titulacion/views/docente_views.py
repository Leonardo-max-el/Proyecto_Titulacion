from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app_titulacion.models import Docente
from django.contrib import messages

@login_required
def inicio_docente(request):
    try:
        docente = Docente.objects.get(user=request.user)
        return render(request, 'docente/inicio_docente.html', {
            'docente': docente
        })
    except Docente.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de docente.')
        return redirect('login')
