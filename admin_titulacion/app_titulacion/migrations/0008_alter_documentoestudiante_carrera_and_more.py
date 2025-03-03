# Generated by Django 5.1.6 on 2025-02-28 19:22

import app_titulacion.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_titulacion', '0007_documentoestudiante_estado_carrera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentoestudiante',
            name='carrera',
            field=models.CharField(choices=[('Derecho', 'Derecho'), ('Ing. Sistemas', 'Ing. Sistemas'), ('Agronomía', 'Agronomía'), ('Veterinaria', 'Veterinaria')], default='pendiente', max_length=50),
        ),
        migrations.AlterField(
            model_name='documentoestudiante',
            name='dni_1',
            field=models.FileField(blank=True, null=True, upload_to=app_titulacion.models.estudiante_directory_path),
        ),
    ]
