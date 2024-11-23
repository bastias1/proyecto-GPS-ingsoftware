from django.db import models
from django.contrib.auth.models import User

# Modelo Vehiculo
class Vehiculo(models.Model):
    patente = models.CharField(max_length=6, unique=True)  # Patente única
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anno = models.IntegerField()

    def __str__(self):
        return f"{self.patente} - {self.modelo} ({self.anno})"

<<<<<<< HEAD
=======
# Modelo GPS
class GPS(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return f"GPS({self.latitud}, {self.longitud})"
>>>>>>> d6c235fb62856b7865bfecf5a0e0f5ffd2457f70

# Modelo Conductor
class Conductor(models.Model):
    ESTADOS_CONDUCTOR = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    estado = models.CharField(max_length=10, choices=ESTADOS_CONDUCTOR)  # Usar opciones predefinidas
    vehiculo_relacionado = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)

    def ultima_posicion(self):
        """Obtiene la última posición GPS del conductor."""
        ultimo_log = self.gps_logs.order_by('-timestamp').first()
        if ultimo_log:
            return {'latitud': ultimo_log.latitud, 'longitud': ultimo_log.longitud, 'timestamp': ultimo_log.timestamp}
        return None

    def __str__(self):
        return f"Conductor asociado al vehículo {self.vehiculo_relacionado}"


# Modelo para registrar posiciones GPS
class GPSLog(models.Model):
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE, related_name='gps_logs')
    latitud = models.FloatField()
    longitud = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Guarda automáticamente la fecha y hora de creación

    def __str__(self):
        return f"{self.conductor} - {self.latitud}, {self.longitud} @ {self.timestamp}"


# Modelo Usuario
class Usuario(models.Model): 
    # Opciones para el tipo de usuario
    TIPO_USUARIO = [
        ('', 'Seleccione un tipo de usuario'),
        ('Administrador', 'Administrador'),
        ('Conductor', 'Conductor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Modelo user tiene los siguientes datos (Nombre, Apellido, Correo, Usuario, Contraseña, Fecha de Creación)
    rut = models.CharField(max_length=10, unique=True)
    telefono = models.BigIntegerField()
    tipo_usuario = models.CharField(max_length=50, choices=TIPO_USUARIO)
    conductor_relacionado = models.OneToOneField(Conductor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.email}"
    
    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()

    def deleteConductor(self, *args, **kwargs):
        user = self.user
        conductor = self.conductor_relacionado
        super().delete(*args, **kwargs)
        user.delete()
        conductor.delete()