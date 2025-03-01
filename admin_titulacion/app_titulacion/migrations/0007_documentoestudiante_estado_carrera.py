# Generated by Django 5.1.6 on 2025-02-28 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_titulacion', '0006_remove_documentoestudiante_boucher_pago_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentoestudiante',
            name='estado_carrera',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('corregir', 'Requiere Corrección')], default='pendiente', max_length=10),
        ),
    ]
