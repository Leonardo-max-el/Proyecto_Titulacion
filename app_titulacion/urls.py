from django.contrib import admin
from django.urls import path

from django import views
from app_titulacion.views import auth_views,estudiante_views
from app_titulacion.views import index_views,grados_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('index', index_views.index, name='index'),
    path('', auth_views.register , name='register'),
    path('login/', auth_views.custom_login_view, name='login'),
    path('clouses',auth_views.clouses, name="clouses"),
    path('inicio_titulacion/', estudiante_views.inicio_titulacion, name='inicio_titulacion'),
    path('modalidad_titulacion/', estudiante_views.modalidad_titulacion, name='modalidad_titulacion'),
    path('modalidad_1', estudiante_views.modalidad_1, name="modalidad_1"),
    path('modalidad_2', estudiante_views.modalidad_2, name="modalidad_2"),
    path('seleccion_modalidad/', estudiante_views.seleccion_modalidad, name='seleccion_modalidad'),
    path('lista_estudiantes', grados_views.lista_estudiantes, name='lista_estudiantes'),
    path('validar/<int:estudiante_id>/', grados_views.validar_documentos, name='validar_documentos'),
] 
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)