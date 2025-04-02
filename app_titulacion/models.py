from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

class User(AbstractUser):
    def __str__(self):
        return self.username

class Estudiante(models.Model):
    ESCUELA_CHOICES = [
        ('Derecho', 'Derecho'),
        ('Ing. Sistemas', 'Ing. Sistemas'),
        ('Agronomía', 'Agronomía'),
        ('Veterinaria', 'Veterinaria'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100, null=False, default='')
    apellido_paterno = models.CharField(max_length=100, null=False, default='')
    apellido_materno = models.CharField(max_length=100, null=False, default='')
    escuela_profesional = models.CharField(max_length=50, choices=ESCUELA_CHOICES, default='Derecho')
    direccion = models.CharField(max_length=200, default='')
    email = models.EmailField(unique=True)
    telefono = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{9}$', message='Teléfono debe contener 9 dígitos')],
        default=''
    )

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellido_paterno}"

class Expediente(models.Model):
    ESTADO_CHOICES = [
        ('en_proceso', 'En Proceso'),
        ('observado', 'Observado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado')
    ]

    MODALIDAD_CHOICES = [
        ('trabajo_suficiencia', 'Trabajo de Suficiencia Profesional'),
        ('trabajo_investigacion_individual', 'Trabajo de Investigación - Individual'),
        ('trabajo_investigacion_grupal', 'Trabajo de Investigación - Grupal')
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='expedientes')
    codigo_expediente = models.CharField(max_length=20, unique=True)
    modalidad = models.CharField(max_length=50, choices=MODALIDAD_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='en_proceso')
    observaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.codigo_expediente:
            año = timezone.now().year
            ultimo_expediente = Expediente.objects.filter(
                codigo_expediente__startswith=f'EXP-{año}'
            ).order_by('-codigo_expediente').first()
            
            if ultimo_expediente:
                ultimo_numero = int(ultimo_expediente.codigo_expediente.split('-')[-1])
                nuevo_numero = ultimo_numero + 1
            else:
                nuevo_numero = 1
            
            self.codigo_expediente = f'EXP-{año}-{nuevo_numero:04d}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_expediente} - {self.estudiante.nombre_completo}"

    class Meta:
        ordering = ['-fecha_creacion']

class Documento(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('dni', 'DNI'),
        ('solicitud', 'Solicitud de Título'),
        ('declaracion_jurada', 'Declaración Jurada'),
        ('constancia_egresado', 'Constancia de Egresado'),
        ('certificado_estudios', 'Certificado de Estudios'),
        ('trabajo_investigacion', 'Trabajo de Investigación'),
        ('recibo_pago', 'Recibo de Pago'),
        ('foto', 'Fotografía'),
        ('otros', 'Otros Documentos')
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('observado', 'Observado')
    ]

    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    archivo = models.FileField(upload_to='documentos/%Y/%m/%d/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observaciones = models.TextField(blank=True, null=True)
    version = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.get_tipo_documento_display()} - {self.expediente.codigo_expediente}"

    class Meta:
        ordering = ['-fecha_subida']
        unique_together = ['expediente', 'tipo_documento', 'version']

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo documento
            ultimo_documento = Documento.objects.filter(
                expediente=self.expediente,
                tipo_documento=self.tipo_documento
            ).order_by('-version').first()
            
            if ultimo_documento:
                self.version = ultimo_documento.version + 1

        super().save(*args, **kwargs)

    def get_document_fields(self):
        """Retorna una lista de campos de documento con sus estados y valores"""
        fields = []
        document_fields = [
            ('dni_1', 'DNI (Frente)'),
            ('dni_2', 'DNI (Reverso)'),
            ('tesis', 'Tesis'),
            ('declaracion_jurada', 'Declaración Jurada'),
            ('copia_bachiller_1', 'Copia de Bachiller (Frente)'),
            ('copia_bachiller_2', 'Copia de Bachiller (Reverso)'),
            ('boucher_pago_1', 'Boucher de Pago (Frente)'),
            ('boucher_pago_2', 'Boucher de Pago (Reverso)'),
            ('solicitud_1', 'Solicitud (Frente)'),
            ('solicitud_2', 'Solicitud (Reverso)'),
        ]
        
        for field_name, label in document_fields:
            field = {
                'name': field_name,
                'label': label,
                'value': getattr(self, field_name),
                'estado': getattr(self, f'estado_{field_name}'),
                'observaciones': getattr(self, f'observaciones_{field_name}', '')
            }
            fields.append(field)
        
        return fields

def estudiante_directory_path(instance, filename):
    return f'documentos/{instance.user.username}/{filename}'

ESTADO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aprobado', 'Aprobado'),
    ('corregir', 'Requiere Corrección'),
]

class Docente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='DNI debe contener 8 dígitos')]
    )
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{9}$', message='Teléfono debe contener 9 dígitos')]
    )
    correo_institucional = models.EmailField(
        unique=True,
        help_text='Correo institucional del docente'
    )
    codigo_doctor = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text='Código único de identificación como doctor (opcional)'
    )
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
        ordering = ['apellido_paterno', 'apellido_materno']

    def __str__(self):
        return f"Dr. {self.apellido_paterno} {self.apellido_materno}"

    @property
    def nombre_completo(self):
        return f"{self.user.first_name} {self.apellido_paterno} {self.apellido_materno}"

class Administrativo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{8}$', message='DNI debe contener 8 dígitos')]
    )
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{9}$', message='Teléfono debe contener 9 dígitos')]
    )
    correo_institucional = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Administrativo'
        verbose_name_plural = 'Administrativos'
        ordering = ['apellido_paterno', 'apellido_materno']

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno}"

    @property
    def nombre_completo(self):
        return f"{self.user.first_name} {self.apellido_paterno} {self.apellido_materno}"

