from django.db import models
from django.contrib.auth.models import User

def estudiante_directory_path(instance, filename):
    return f'documentos/{instance.estudiante.username}/{filename}'

ESTADO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aprobado', 'Aprobado'),
    ('corregir', 'Requiere Corrección'),
]

class DocumentoEstudiante(models.Model):
    MODALIDAD_CHOICES = [
        ('modalidad_1', 'Modalidad 1'),
        ('modalidad_2', 'Modalidad 2'),
    ]

    CARRERA_CHOICES = [
        ('Derecho', 'Derecho'),
        ('Ing. Sistemas', 'Ing. Sistemas'),
        ('Agronomía', 'Agronomía'),
        ('Veterinaria', 'Veterinaria'),
    ]

    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)

    # Campo de carrera con estado
    carrera = models.CharField(max_length=50, choices=CARRERA_CHOICES, default='pendiente')
    estado_carrera = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # Documentos del estudiante con estado de validación
    dni_1 = models.FileField(upload_to=estudiante_directory_path, blank=True, null=True)
    estado_dni_1 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    dni_2 = models.FileField(upload_to=estudiante_directory_path, blank=True, null=True)
    estado_dni_2 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # tesis = models.FileField(upload_to=estudiante_directory_path)
    # estado_tesis = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # declaracion_jurada = models.FileField(upload_to=estudiante_directory_path, blank=True, null=True)
    # estado_declaracion_jurada = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # copia_bachiller_1 = models.FileField(upload_to=estudiante_directory_path, default='', blank=True, null=True)
    # estado_copia_bachiller_1 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # boucher_pago_1 = models.FileField(upload_to=estudiante_directory_path)
    # estado_boucher_pago_1 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # copia_bachiller_2 = models.FileField(upload_to=estudiante_directory_path, blank=True, null=True)
    # estado_copia_bachiller_2 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # boucher_pago_2 = models.FileField(upload_to=estudiante_directory_path, blank=True, null=True)
    # estado_boucher_pago_2 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # solicitud_1 = models.FileField(upload_to=estudiante_directory_path, blank=True, null=True)
    # estado_solicitud_1 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    # solicitud_2 = models.FileField(upload_to=estudiante_directory_path, blank=True, null=True)
    # estado_solicitud_2 = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def save(self, *args, **kwargs):
        # Si la modalidad es 1, vaciar los campos extra de modalidad 2
        if self.modalidad == 'modalidad_1':
            self.dni_2 = None
            # self.estado_dni_2 = 'pendiente'
            # self.solicitud_2 = None
            # self.estado_solicitud_2 = 'pendiente'
            # self.copia_bachiller_2 = None
            # self.estado_copia_bachiller_2 = 'pendiente'
            # self.boucher_pago_2 = None
            # self.estado_boucher_pago_2 = 'pendiente'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.estudiante.username} - {self.modalidad} - {self.carrera}"
