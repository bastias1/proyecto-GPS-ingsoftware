# Generated by Django 5.1.3 on 2024-11-22 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_conductor_nombre_remove_usuario_apellido_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conductor',
            name='fecha_creacion',
        ),
    ]
