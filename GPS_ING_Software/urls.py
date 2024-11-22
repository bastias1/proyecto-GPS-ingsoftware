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
from django.urls import path
from app import views as views
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),


    path('login/',views.inicioSesion,name='login'),
    path('logout/',views.cerrarSesion,name='logout'),
    path('dashboard/',views.dashboard,name = 'dashboard'),

    #menus
    path('mapa/',views.mapa,name = 'mapa'),

    #Empleados
    path('usuarios/',views.gestionUsuarios,name='usuarios'),
    path('crearUsuario/',views.creacionUsuario,name='creacionUsuario'),
    path('modificarUsuario/<int:id>/',views.modificarUsuario,name='modificarUsuario'),
    path('eliminarUsuario/<int:id>/',views.eliminarUsuario,name='eliminarUsuario'),
]
