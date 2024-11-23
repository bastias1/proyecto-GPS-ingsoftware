from django.contrib import admin
from .models import GPSLog, Conductor, Vehiculo

admin.site.register(GPSLog)
admin.site.register(Conductor)
admin.site.register(Vehiculo)