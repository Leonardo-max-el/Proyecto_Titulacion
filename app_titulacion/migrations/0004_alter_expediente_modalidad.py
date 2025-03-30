# Generated by Django 5.1.6 on 2025-03-30 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_titulacion', '0003_expediente_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expediente',
            name='modalidad',
            field=models.CharField(choices=[('trabajo_suficiencia', 'Trabajo de Suficiencia Profesional'), ('trabajo_investigacion_individual', 'Trabajo de Investigación - Individual'), ('trabajo_investigacion_grupal', 'Trabajo de Investigación - Grupal')], max_length=50),
        ),
    ]
