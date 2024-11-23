from django.shortcuts import render,redirect
from django.http import Http404,JsonResponse
from .models import *
from . import forms 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
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
    conductores = Usuario.objects.filter(tipo_usuario='Conductor')
    context = {'conductores': conductores}
    return render(request, 'mapa.html', context)


# API para devolver datos GPS en formato JSON
def api_gps_data(request):
    logs = GPSLog.objects.select_related('conductor').all()
    data = []
    
    for log in logs:
        data.append({
            "id": log.conductor.id if log.conductor else None,
            "latitud": log.latitud,
            "longitud": log.longitud,
            "estado": log.conductor.estado if log.conductor else "Desconocido",
            "timestamp": log.timestamp.isoformat(),
        })
    
    return JsonResponse(data, safe=False)


@csrf_exempt
def owntracks_webhook(request):
    if request.method == "POST":
        try:
            # Log raw request body for debugging
            print("Raw Request Body:", request.body)

            # Parse JSON data
            data = json.loads(request.body)

            # Log parsed data for debugging
            print("Parsed Data:", data)

            # Extract data (ensure it matches your payload)
            user_id = data.get("user")
            lat = data.get("lat")
            lon = data.get("lon")

            timestamp = data.get("tst")
            if timestamp:
                timestamp = now().fromtimestamp(timestamp)

            # Find the corresponding Usuario by username
            try:
                usuario = Usuario.objects.get(user__username=user_id)
            except Usuario.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=404)

            # Create a GPSLog entry
            GPSLog.objects.create(
                conductor=usuario,
                latitud=lat,
                longitud=lon,
                timestamp=timestamp or now()
            )

            # Debugging logs
            if not user_id:
                return JsonResponse({"error": "Missing 'user' field"}, status=400)
            if not lat or not lon:
                return JsonResponse({"error": "Missing 'lat' or 'lon' field"}, status=400)

            # Return success for testing
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)



#Empleados
def gestionUsuarios(request):
    usuarios = Usuario.objects.filter(tipo_usuario='Administrador')
    
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
        if form.is_valid():
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
    usuarios = Usuario.objects.filter(tipo_usuario='Conductor').prefetch_related('vehiculos')

    data = {
        'usuarios':usuarios
    }

    return render(request,'gestionConductores.html',data)

def crearConductor(request):
    if request.method=='POST':
        form_user = forms.registroUser(request.POST)
        form_usuario = forms.registroUsuario(request.POST)
        if form_usuario.is_valid() and form_user.is_valid():
            user = form_user.save(commit=False)
            user.set_password(form_user.cleaned_data['password'])
            user.save()
            usuario = form_usuario.save(commit=False)
            usuario.tipo_usuario = 'Conductor'
            usuario.user = user
            usuario.save()
            return redirect('conductores')  # Redirigir a la URL raíz
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

    return render(request,'crearConductor.html',data)


def modificarConductor(request,id):
    conductor = User.objects.get(id=id) # Obtener el vehículo
    conductor1 = Usuario.objects.get(id=id)
    

    # Si el formulario es enviado (POST)
    if request.method == 'POST':
        form_user = forms.registroUser(request.POST, instance=conductor)  # Usamos el formulario con la instancia
        form_usuario = forms.registroUsuario(request.POST, instance=conductor)
        if form_user.is_valid() and form_usuario.is_valid():
            form_user.save()
            form_usuario.save()  # Guardamos los cambios en la base de datos
            return redirect('conductores')  # Redirigimos después de guardar
    else:
        form_user = forms.registroUser(instance=conductor) 
        form_usuario = forms.registroUsuario(instance=conductor1)   # Para GET, solo pasamos la instancia

    data = {
        'form_usuario':form_usuario,
        'form_user':form_user,
        }
    return render(request, 'crearConductor.html', data)

def eliminarConductor(request,id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('conductores')