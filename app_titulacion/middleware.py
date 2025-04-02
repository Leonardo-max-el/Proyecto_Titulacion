from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

class SessionManagementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Obtener la sesión actual
            current_session_key = request.session.session_key
            
            # Limpiar sesiones expiradas
            Session.objects.filter(expire_date__lt=timezone.now()).delete()
            
            # Obtener todas las sesiones activas del usuario
            user_sessions = Session.objects.filter(
                expire_date__gt=timezone.now()
            ).order_by('-expire_date')
            
            # Verificar si el usuario tiene demasiadas sesiones activas
            max_sessions = getattr(settings, 'MAX_SESSIONS_PER_USER', 5)
            
            if user_sessions.count() > max_sessions:
                # Eliminar las sesiones más antiguas
                for session in user_sessions[max_sessions:]:
                    session.delete()
            
            # Actualizar la última actividad
            request.session['last_activity'] = timezone.now().isoformat()
            
            # Verificar tiempo de inactividad
            if 'last_activity' in request.session:
                last_activity = timezone.datetime.fromisoformat(request.session['last_activity'])
                inactivity_period = timezone.now() - last_activity
                max_inactivity = getattr(settings, 'SESSION_INACTIVITY_TIMEOUT', 3600)  # 1 hora
                
                if inactivity_period.total_seconds() > max_inactivity:
                    logout(request)
                    messages.warning(request, 'Tu sesión ha expirado por inactividad.')
                    return HttpResponseRedirect(reverse('login'))

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Excluir algunas URLs del control de sesión
        excluded_paths = [
            reverse('login'),
            reverse('logout'),
            # Agrega aquí otras URLs que quieras excluir
        ]
        
        if request.path in excluded_paths:
            return None
            
        return None
