from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from django import views
from app_titulacion.views import auth_views,estudiante_views, docente_views 
from app_titulacion.views import index_views,grados_views
from django.conf import settings
from django.conf.urls.static import static
from .views.admin_views import lista_usuarios, crear_usuario, editar_usuario, eliminar_usuario
from . import views

urlpatterns = [
    path('docente/expedientes/', docente_views.lista_expedientes, name='lista_expedientes_docente'),
    path('index', index_views.index, name='index'),
    path('', auth_views.register , name='register'),
    path('login/', auth_views.custom_login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('clouses',auth_views.clouses, name="clouses"),
    path('inicio_titulacion/', estudiante_views.inicio_titulacion, name='inicio_titulacion'),
    path('crear_expediente/', estudiante_views.crear_expediente, name='crear_expediente'),
    path('gestionar_expediente/<int:expediente_id>/', estudiante_views.gestionar_expediente, name='gestionar_expediente'),
    
    # Nuevas URLs para la gestión de expedientes
    path('lista_expedientes/', grados_views.lista_expedientes, name='lista_expedientes'),
    path('gestionar_expediente_admin/<int:expediente_id>/', grados_views.gestionar_expediente_admin, name='gestionar_expediente_admin'),
    path('actualizar-observaciones/<int:documento_id>/', grados_views.actualizar_observaciones, name='actualizar_observaciones'),
    path('responder-mensaje/<int:mensaje_id>/', grados_views.responder_mensaje, name='responder_mensaje'),

    path('lista_usuarios/', lista_usuarios, name='lista_usuarios'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:user_id>/', editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
    
    path('inicio_docente/', docente_views.inicio_docente, name='inicio_docente'),
] 
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)