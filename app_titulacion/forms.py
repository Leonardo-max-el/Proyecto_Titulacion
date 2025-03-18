from django import forms
from .models import DocumentoEstudiante

class EstudianteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = DocumentoEstudiante
        fields = ['nombre', 'email', 'password','Gnero']
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo Electrónico',
            'Gnero':'genero',
            'password': 'Contraseña'
        }