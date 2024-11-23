from django.shortcuts import render,redirect
from django.http import Http404,JsonResponse
from .models import *
from . import forms 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    return render(request,'login.html')

def inicioSesion(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.success(request,("Hubo un error al iniciar sesion."))
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def cerrarSesion(request):
    logout(request)
    messages.success(request,("Se a cerrado la sesion."))
    return redirect('login')

def dashboard(request):
    return render(request, 'dashboard.html')

def mapa(request):
    conductores = Conductor.objects.all()  # Obtener todos los conductores
    context = {'conductores': conductores}
    return render(request, 'mapa.html', context)


# API para devolver datos GPS en formato JSON
def api_gps_data(request):
    logs = GPSLog.objects.select_related('conductor').all()
    print("Datos encontrados:", logs)  # Este mensaje aparecerá en la consola del servidor
    data = [
        {
            "conductor": log.conductor.vehiculo_relacionado.patente if log.conductor.vehiculo_relacionado else "Sin Vehículo",
            "latitud": log.latitud,
            "longitud": log.longitud,
            "vehiculo": log.conductor.vehiculo_relacionado.modelo if log.conductor.vehiculo_relacionado else "No asignado",
            "estado": log.conductor.estado,
            "timestamp": log.timestamp.isoformat(),
        }
        for log in logs
    ]
    return JsonResponse(data, safe=False)



# Endpoint para recibir datos GPS desde OwnTracks
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import GPSLog, Conductor, Vehiculo

@csrf_exempt
def receive_owntracks_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Busca al conductor asociado (puedes usar username o identificador único del dispositivo)
            conductor = Conductor.objects.get(vehiculo_relacionado__patente=data.get('tid'))
            # Guarda la ubicación
            GPSLog.objects.create(
                conductor=conductor,
                latitud=data['lat'],
                longitud=data['lon'],
            )
            return JsonResponse({"status": "success"}, status=201)
        except Conductor.DoesNotExist:
            return JsonResponse({"error": "Conductor no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos inválidos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)




#Empleados
def gestionUsuarios(request):
    usuarios = Usuario.objects.filter(conductor_relacionado__isnull=True)
    
    data = {
        'usuarios':usuarios
    }
    return render(request, 'gestionUsuarios.html',data)

def creacionUsuario(request):
    if request.method=='POST':
        form_user = forms.registroUser(request.POST)
        form_usuario = forms.registroUsuario(request.POST)
        print("Form Insertado")
        if form_usuario.is_valid() and form_user.is_valid():
            print("Datos insertados a la base de datos")
            user = form_user.save(commit=False)
            user.set_password(form_user.cleaned_data['password'])
            user.save()
            usuario = form_usuario.save(commit=False)
            usuario.tipo_usuario = 'Administrador'
            usuario.user = user
            usuario.save()
            return redirect('usuarios')  # Redirigir a la URL raíz
        else:
            print("Errores en los formularios")
    else:
        print("Datos NO insertados")
        form_user = forms.registroUser()
        form_usuario = forms.registroUsuario()
    
    data = {
        'form_usuario':form_usuario,
        'form_user':form_user,
    }
    return render(request,'crearUsuarios.html',data)

def modificarUsuario(request,id):
    # Obtener el empleado por ID
    usuario = Usuario.objects.get(id=id)
    user = usuario.user  # Obtener el usuario asociado

    # Formularios prellenados con los datos actuales
    form_usuario = forms.registroUsuario(instance=usuario)
    form_user = forms.registroUser(instance=user)

    if request.method == "POST":
        # Actualizar datos de empleado y usuario
        form_usuario = forms.registroUsuario(request.POST, instance=usuario)
        form_user = forms.registroUser(request.POST, instance=user)

        if form_usuario.is_valid() and form_user.is_valid():
            # Guardar datos de usuario y empleado
            user = form_user.save(commit=False)
            if form_user.cleaned_data.get('password'):
                user.set_password(form_user.cleaned_data['password'])
            user.save()

            usuario = form_usuario.save(commit=False)
            usuario.user = user
            usuario.save()

            print("Usuario modificado correctamente")
            return redirect('usuarios')  # Redirige al listado de empleados

    data = {
        'form_usuario': form_usuario,
        'form_user': form_user,
        'es_modificar': True,  # Variable de contexto para diferenciar
        'usuario': usuario,
    }
    return render(request, 'crearUsuarios.html', data)

def eliminarUsuario(request,id):
    if User.objects.count() <= 1:
        messages.success(request,("No se puede eliminar el último usuario"))
        return redirect('usuarios')
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    print("Usuario Eliminado")
    return redirect('usuarios')



#GESTIONAR VEHICULOS

def gestionVehiculos(request):
    vehiculos = Vehiculo.objects.all()
    
    data = {
        'vehiculos':vehiculos
    }
    return render(request, 'gestionVehiculos.html',data)


def crearVehiculo(request):
    if request.method == 'POST':
        form = forms.registroVehiculo(request.POST)
        print("Form insertado")
        if form.is_valid():
            print("Datos ingresados correctamente")
            form.save()
            return redirect('/vehiculos')
    else:
        form = forms.registroVehiculo()

    data = {'form': form}
    return render(request, 'crearVehiculo.html', data)


def eliminarVehiculo(request, id):
    try:
        vehiculo = Vehiculo.objects.get(id=id)
        vehiculo.delete()
    except Vehiculo.DoesNotExist:
        pass
    return redirect('/vehiculos')

def modificarVehiculo(request, id):
    vehiculo = Vehiculo.objects.get(id=id)  # Obtener el vehículo

    # Si el formulario es enviado (POST)
    if request.method == 'POST':
        form = forms.registroVehiculo(request.POST, instance=vehiculo)  # Usamos el formulario con la instancia
        if form.is_valid():
            form.save()  # Guardamos los cambios en la base de datos
            return redirect('/vehiculos')  # Redirigimos después de guardar
    else:
        form = forms.registroVehiculo(instance=vehiculo)  # Para GET, solo pasamos la instancia

    data = {'form': form}
    return render(request, 'crearVehiculo.html', data)


#Gestionar Conductores

def gestionConductores(request):
    usuarios = Usuario.objects.filter(conductor_relacionado__isnull=False)

    data = {
        'usuarios':usuarios
    }
    return render(request,'gestionConductores.html',data)

def crearConductor(request):
    if request.method=='POST':
        form_user = forms.registroUser(request.POST)
        form_usuario = forms.registroUsuario(request.POST)
        form_conductor = forms.registroConductor(request.POST)
        print("Form Insertado")
        if form_usuario.is_valid() and form_user.is_valid() and form_conductor.is_valid():
            print("Datos insertados a la base de datos")
            conductor = form_conductor.save()
            user = form_user.save(commit=False)
            user.set_password(form_user.cleaned_data['password'])
            user.save()
            usuario = form_usuario.save(commit=False)
            usuario.tipo_usuario = 'Conductor'
            usuario.conductor_relacionado = conductor
            usuario.user = user
            usuario.save()
            return redirect('conductores')  # Redirigir a la URL raíz
        else:
            print("Errores en los formularios")
    else:
        print("Datos NO insertados")
        form_user = forms.registroUser()
        form_usuario = forms.registroUsuario()
        form_conductor = forms.registroConductor(request.POST)
    
    data = {
        'form_usuario':form_usuario,
        'form_user':form_user,
        'form_conductor':form_conductor,
    }

    return render(request,'crearConductor.html',data)


def modificarConductor(request,id):
    pass

def eliminarConductor(request,id):
    usuario = Usuario.objects.get(id=id)
    usuario.deleteConductor()
    print("Usuario Eliminado")
    return redirect('conductores')