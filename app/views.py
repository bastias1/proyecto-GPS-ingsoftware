from django.shortcuts import render
from django.http import Http404
from .models import GPS, Conductor, Vehiculo

# Create your views here.
def index(request):
    return render(request,'login.html')


def adminDashboard(request):
    conductores = Conductor.objects.all()  # Obtener todos los conductores
    gps = GPS.objects.all()  # Obtener todos los GPS (o filtrar según sea necesario)
    vehiculos = Vehiculo.objects.all()  # Obtener todos los vehículos

    context = {
        'conductores': conductores,
        'gps': gps,
        'vehiculos': vehiculos,
    }
    return render(request, 'dashboardMain.html', context)