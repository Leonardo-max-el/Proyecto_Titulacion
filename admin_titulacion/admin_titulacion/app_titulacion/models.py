from django.db import models

# Create your models here.
class DocumentoEstudiante(models.Model):
    MODALIDAD_CHOICES = [
        ('modalidad_1', 'Modalidad 1'),
        ('modalidad_2', 'Modalidad 2'),
    ]


    
    
    estudiante = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)
    dni = models.FileField(upload_to='documentos/dni/')
    pago = models.FileField(upload_to='documentos/pago/')
    tesis = models.FileField(upload_to='documentos/tesis/')
    declaracion_jurada = models.FileField(upload_to='documentos/declaracion_jurada/', blank=True, null=True)
    
    # Campos específicos por modalidad
    copia_bachiller_1 = models.FileField(upload_to='documentos/copia_bachiller/')
    boucher_pago_1 = models.FileField(upload_to='documentos/boucher_pago/')
    
    # Solo si es modalidad_2
    copia_bachiller_2 = models.FileField(upload_to='documentos/copia_bachiller/', blank=True, null=True)
    boucher_pago_2 = models.FileField(upload_to='documentos/boucher_pago/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Si la modalidad es 1, vaciar los campos extra de modalidad 2
        if self.modalidad == 'modalidad_1':
            self.copia_bachiller_2 = None
            self.boucher_pago_2 = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.modalidad}"