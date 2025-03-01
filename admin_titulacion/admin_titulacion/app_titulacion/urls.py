from django.contrib import admin
from django.urls import path

from django import views
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.register, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('clouses',views.clouses, name="clouses"),
    path('modalidad_1', views.modalidad_1, name="modalidad_1"),
    path('modalidad_2', views.modalidad_2, name="modalidad_2"),
    path('seleccion_modalidad/', views.seleccion_modalidad, name='seleccion_modalidad')
]