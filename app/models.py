from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Modelo Vehiculo
class Vehiculo(models.Model):
    patente = models.CharField(max_length=6, unique=True)  # Patente única
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anno = models.IntegerField()

    def __str__(self):
        return f"{self.patente} - {self.modelo} ({self.anno})"




# Modelo GPS
class GPS(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return f"GPS({self.latitud}, {self.longitud})"

# Modelo Conductor
class Conductor(models.Model):
    ESTADOS_CONDUCTOR = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    estado = models.CharField(max_length=10, choices=ESTADOS_CONDUCTOR)  # Usar opciones predefinidas
    vehiculo_relacionado = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    gps = models.ForeignKey(GPS, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo Usuario
class Usuario(models.Model): 
    # Opciones para el tipo de usuario
    TIPO_USUARIO = [
        ('', 'Seleccione un tipo de usuario'),
        ('Administrador', 'Administrador'),
        ('Conductor', 'Conductor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE) #Modelo user tiene los siguientes datos (Nombre, Apellido, Correo, Usuario, Contraseña, Fecha de Creacion)
    rut = models.CharField(max_length=10,unique=True)
    telefono = models.BigIntegerField()
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO)
    conductor_relacionado = models.ForeignKey(Conductor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.apellido}, {self.correo}"
    
    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()
