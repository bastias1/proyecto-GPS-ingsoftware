"""
URL configuration for GPS_ING_Software project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app import views as views
from app.views import *

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Vistas principales
    path('', views.index),

    # Sesión
    path('login/', views.inicioSesion, name='login'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Menús
    path('mapa/', views.mapa, name='mapa'),

    # Empleados
    path('usuarios/', views.gestionUsuarios, name='usuarios'),
    path('crearUsuario/', views.creacionUsuario, name='creacionUsuario'),
    path('modificarUsuario/<int:id>/', views.modificarUsuario, name='modificarUsuario'),
    path('eliminarUsuario/<int:id>/', views.eliminarUsuario, name='eliminarUsuario'),

    # Vehículos
    path('vehiculos/', views.gestionVehiculos, name='vehiculos'),
    path('crearVehiculo/', views.crearVehiculo, name='crearVehiculo'),
    path('modificarVehiculo/<int:id>/', views.modificarVehiculo, name='modificarVehiculo'),
    path('eliminarVehiculo/<int:id>/', views.eliminarVehiculo, name='eliminarVehiculo'),

    # GPS Data
    path('api/owntracks/', views.receive_owntracks_data, name='owntracks'),  # Principal endpoint para OwnTracks
    path('api/gps-data/', views.api_gps_data, name='api_gps_data'),  # Datos para el mapa
]
