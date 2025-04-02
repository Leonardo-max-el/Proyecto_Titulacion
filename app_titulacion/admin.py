from django.contrib import admin
from .models import Docente, Administrativo

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ['dni', 'apellido_paterno', 'apellido_materno', 'correo_institucional', 'codigo_doctor']
    search_fields = ['dni', 'apellido_paterno', 'apellido_materno', 'correo_institucional', 'codigo_doctor']
    list_filter = ['fecha_registro']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    fieldsets = (
        ('Información Personal', {
            'fields': ('user', 'dni', 'apellido_paterno', 'apellido_materno', 'direccion')
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'correo_institucional')
        }),
        ('Información Profesional', {
            'fields': ('codigo_doctor',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Administrativo)
class AdministrativoAdmin(admin.ModelAdmin):
    list_display = ['dni', 'apellido_paterno', 'apellido_materno', 'correo_institucional']
    search_fields = ['dni', 'apellido_paterno', 'apellido_materno', 'correo_institucional']
    list_filter = ['fecha_registro']
