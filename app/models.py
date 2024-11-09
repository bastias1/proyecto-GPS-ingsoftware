from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Modelo Vehiculo
class Vehiculo(models.Model):
    patente = models.CharField(max_length=6, unique=True)  # Patente única
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

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, choices=ESTADOS_CONDUCTOR)  # Usar opciones predefinidas
    fecha_creacion = models.DateTimeField(default=timezone.now)
    vehiculo_relacionado = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    gps = models.ForeignKey(GPS, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

# Opciones para el tipo de usuario
TIPO_USUARIO = [
    ('', 'Seleccione un tipo de usuario'),
    ('Administrador', 'Administrador'),
    ('Conductor', 'Conductor'),
]

# Modelo Usuario
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=30)
    correo = models.EmailField(unique=True)  # Correo único
    contraseña = models.CharField(max_length=128)
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO)
    conductor_relacionado = models.ForeignKey(Conductor, on_delete=models.CASCADE, null=True, blank=True)

    def crear_contraseña(self, raw_password):
        self.contraseña = make_password(raw_password)  # Encriptar la contraseña
        self.save()

    def __str__(self):
        return f"{self.apellido}, {self.correo}"