from django.shortcuts import render,redirect
from django.http import Http404
from .models import *
from . import forms 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    gps = GPS.objects.all()  # Obtener todos los GPS (o filtrar según sea necesario)
    vehiculos = Vehiculo.objects.all()  # Obtener todos los vehículos

    context = {
        'conductores': conductores,
        'gps': gps,
        'vehiculos': vehiculos,
    }
    return render(request, 'mapa.html', context)


#Empleados
def gestionUsuarios(request):
    usuarios = Usuario.objects.all()
    
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
    if User.objects.count() == 1:
        messages.success(request,("No se puede eliminar el último usuario"))
        return redirect('usuarios')
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    print("Usuario Eliminado")
    return redirect('usuarios')
