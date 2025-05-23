# Generated by Django 5.1.6 on 2025-03-29 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_titulacion', '0002_titulacion_individual_delete_documentoestudiante'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_expediente', models.CharField(max_length=20, unique=True)),
                ('modalidad', models.CharField(choices=[('tesis', 'Tesis'), ('trabajo_suficiencia', 'Trabajo de Suficiencia Profesional'), ('trabajo_investigacion', 'Trabajo de Investigación')], max_length=50)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(choices=[('en_proceso', 'En Proceso'), ('enviado', 'Enviado'), ('observado', 'Observado'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], default='en_proceso', max_length=20)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expedientes', to='app_titulacion.estudiante')),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(choices=[('dni', 'DNI'), ('solicitud', 'Solicitud de Título'), ('declaracion_jurada', 'Declaración Jurada'), ('constancia_egresado', 'Constancia de Egresado'), ('certificado_estudios', 'Certificado de Estudios'), ('trabajo_investigacion', 'Trabajo de Investigación'), ('recibo_pago', 'Recibo de Pago'), ('foto', 'Fotografía'), ('otros', 'Otros Documentos')], max_length=50)),
                ('archivo', models.FileField(upload_to='documentos/%Y/%m/%d/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('observado', 'Observado')], default='pendiente', max_length=20)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('version', models.IntegerField(default=1)),
                ('expediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='app_titulacion.expediente')),
            ],
            options={
                'ordering': ['-fecha_subida'],
                'unique_together': {('expediente', 'tipo_documento', 'version')},
            },
        ),
    ]
