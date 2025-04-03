# Generated by Django 5.1.6 on 2025-04-03 04:48

import app_titulacion.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_titulacion', '0011_mensaje'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoMensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to=app_titulacion.models.mensaje_directory_path)),
                ('nombre_archivo', models.CharField(max_length=255)),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('mensaje', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='archivos', to='app_titulacion.mensaje')),
            ],
            options={
                'verbose_name': 'Archivo de Mensaje',
                'verbose_name_plural': 'Archivos de Mensajes',
                'ordering': ['-fecha_subida'],
            },
        ),
    ]
