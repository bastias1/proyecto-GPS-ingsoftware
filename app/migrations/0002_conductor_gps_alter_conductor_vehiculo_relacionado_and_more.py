# Generated by Django 5.1.1 on 2024-11-09 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conductor',
            name='gps',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.gps'),
        ),
        migrations.AlterField(
            model_name='conductor',
            name='vehiculo_relacionado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.vehiculo'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='anno',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='modelo',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=9)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('correo', models.EmailField(max_length=254)),
                ('contraseña', models.CharField(max_length=128)),
                ('tipo_usuario', models.CharField(choices=[('', 'Seleccione un tipo de usuario'), ('Administrador', 'Administrador'), ('Conductor', 'Conductor')], max_length=50)),
                ('conductor_relacionado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.conductor')),
            ],
        ),
    ]
