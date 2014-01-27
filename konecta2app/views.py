#-*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.conf import settings
from konecta2app.models import Permisos, MateriasEjercicios, Dificultad, Notificacion, CursosEjercicios, Tokenregister, Cursos, Profesor, Alumno, Invitado
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from konecta2 import settings
import string
import pytz
import random
import datetime
import json
import base64
from base64 import b64decode
from annoying.functions import get_object_or_None
from konecta2 import config




def file_not_found_404(request):
    #create some variables here if you like
    path = request.path
    response = render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))
    response.status_code = 404
    
    return (response)

def index(request):
    response_data = "index"
    return render_to_response('index.html', response_data, context_instance=RequestContext(request))

def id_generator(size=70, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def usuario_generator(size=10, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

@csrf_exempt
def login(request):
    """
    {
    "data":{
    username:"<username>",
    password:"<password>"
    "lugar":"lugar"

    }

    }
    Con el usuario y el password, hace un inicio de sesión de los usuarios poniendole el estado en Conectado.
    A continuación les crea un token y si ya tenian uno, cambian el anterior por otro nuevo.
    En caso de mandar un usuario o password que no exista da un error.
    """
    random1 = id_generator()
    userlog = []
    try:
        userlog = simplejson.loads(request.POST['data'])
        user = auth.authenticate(username=userlog.get('username'), password=userlog.get('password'))
        finish = 1
        username = userlog.get('username')
        password = userlog.get('password')
        lugar = userlog.get('lugar','null')
        type_user = userlog.get('type')
        username = username.lower()
        if username is None and password is None:
            response_data = {'result': 'fail', 'message': 'Falta el username y el password'}			
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

        if username is None:
            response_data = {'result': 'fail', 'message': 'Falta el username'}				
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


        if password is None:
            response_data = {'result': 'fail', 'message': 'Falta el password'}

        if user is not None:

            auth.login(request, user)
            usuario = User.objects.get(username=username)
            tipo1 = Alumno.objects.filter(idusuario=usuario)
            tipo2 = Profesor.objects.filter(idusuario=usuario)
            if str(user.is_staff) == "True":
                user_token = get_object_or_None(Tokenregister, userid=user)
                if user_token==None:
                    token1 = str(user.id) + "_" + random1
                    tokenform = Tokenregister(token=token1, userid=user)
                    tokenform.save()
                    user_token = get_object_or_None(Tokenregister, userid=user)
                else:
                    if user_token.date+datetime.timedelta(0,finish) < datetime.datetime.now(pytz.utc):
                        user_token.date = datetime.datetime.now(pytz.utc)
                        user_token.token = str(user.id) + "_" + random1
                        user_token.save()
                    token1 = user_token.token
                validity = user_token.date+datetime.timedelta(0,finish)
                response_data = {'result': 'ok', 'token': user_token.token, 'tipo_usuario': 'Profesor', 'validity': str(validity)}          
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

            if tipo1.count() > 0:
                tipo1 = Alumno.objects.get(idusuario=usuario)
                tipo1.estado = "Conectado"
                tipo1.save()
                tipo_usuario = "Alumno"
            if tipo2.count() > 0:
                tipo2 = Profesor.objects.get(idusuario=usuario)
                tipo2.estado = "Conectado"
                tipo2.save()
                tipo_usuario = "Profesor"
            user_token = get_object_or_None(Tokenregister, userid=user)
            if user_token==None:
                token1 = str(user.id) + "_" + random1
                tokenform = Tokenregister(token=token1, userid=user)
                tokenform.save()
                user_token = get_object_or_None(Tokenregister, userid=user)
            else:
                if lugar == "aplicacionpc":
                    token1 = user_token.token
                else:                    
                    if user_token.date+datetime.timedelta(0,finish) < datetime.datetime.now(pytz.utc):
                        user_token.date = datetime.datetime.now(pytz.utc)
                        user_token.token = str(user.id) + "_" + random1
                        user_token.save()
                    token1 = user_token.token
            response_data = {'tipo_usuario':tipo_usuario,'result': 'ok', 'token': token1}			
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        else:
            response_data = {'result': 'fail', 'message': 'Incorrect data'}			
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}		
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def logout(request):
    """
    {
    data:
    {
    "token":"token"
    }
    }
    Con el token busca el usuario y con este mira si es tipo profesor, alumno o invitado.
    Si es profesor o alumno, le pone el estado en desconectado y elimina el token.
    En caso de que el usuario sea invitado, borra el usuario, y su token.
    """
    data = []
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        lugar = data.get('lugar', '')
        user = Tokenregister.objects.filter(token=token)
        if user.count() > 0:
            user_token = Tokenregister.objects.get(token=token)
            usuario_encontrado = User.objects.get(id=user_token.userid.id)

            tipo1 = Alumno.objects.filter(idusuario=usuario_encontrado)
            tipo2 = Profesor.objects.filter(idusuario=usuario_encontrado)
            tipo3 = Invitado.objects.filter(idusuario=usuario_encontrado)
            if tipo1.count() > 0:
                tipo1 = Alumno.objects.get(idusuario=usuario_encontrado)
                tipo1.estado = "Desconectado"
                tipo1.save()

            if tipo2.count() > 0:
                if lugar == "aplicacionpc":
                    response_data = {'result':'ok'}
                    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
                else:
                    tipo2 = Profesor.objects.get(idusuario=usuario_encontrado)
                    tipo2.estado = "Desconectado"
                    tipo2.save()

            if tipo3.count() > 0:
                tipo3 = Invitado.objects.get(idusuario=usuario_encontrado)
                tipo3.curso.clear()
                tipo3.ejercicio.clear()
                usuario_encontrado.delete()
                tipo3.delete()

            user_token.delete()
            response_data = {'result': 'ok'}
        else:
            response_data = {'result': 'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except Exception as e:

        response_data = {'errorcode': 'E000', 'result': 'error', 'message': e.message}		
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def registro(request):
    """
		{
		data:
			{
			"username":"username"
			"password":"password"
			"tipo":"tipo"
			"clases":
				[{"clase":"clase"}]
			"nombre":"nombre"
			"primer_apellido":"primerapellido"
			"segundo_apellido":"segundoapellido"
            "crear_usuario":"crear_usuario"
            "modificar_usuario":"modificar_usuario"
            "eliminar_usuario":"eliminar_usuario"
            "ver_notas":"ver_notas"
            "modificar_notas":"modificar_notas"
            "ver_todos_usuarios":"ver_todos_usuarios"
            "crear_ejercicio":"crear_ejercicio"
            "modificar_ejercicio":"modificar_ejercicio"
            "eliminar_ejercicio":"eliminar_ejercicio"
            "imagen":"imagen"
            "nacimiento":"nacimiento"
			}
		}
    Esta vista crea usuarios. Se hace una comprobación de si el usuario ya existia en la base de datos.
    Si el usuario no existia en la base de datos, lo crea, y le crea su perfil en su correspondiente tabla(alumno
        o profesor).
    En caso de que el usuario sea profesor, también le pone los permisos a este usuario.
    """
    try:

        data = simplejson.loads(request.POST['data'])
        username = data.get('username', 'null')
        password = data.get('password', 'null')
        tipo = data.get('tipo')
        token = data.get('token')
        clases_array = data.get('clases', 'null')
        crear_user = data.get('crear_usuario', 'false')
        mod_user = data.get('modificar_usuario', 'false')
        elimi_user = data.get('eliminar_usuario', 'false')
        ver_nota = data.get('ver_notas', 'false')
        mod_notas = data.get('modificar_notas', 'false')
        nombre = data.get('nombre', '')
        primer_apellido = data.get('primer_apellido', '')
        segundo_apellido = data.get('segundo_apellido', '')
        ver_todos_usuarios = data.get('ver_todos_usuarios', 'false')
        crear_ejercicio = data.get('crear_ejercicios', 'false')
        modificar_ejercicio = data.get('modificar_ejercicios', 'false')
        eliminar_ejercicio = data.get('eliminar_ejercicios', 'false')
        imagen = data.get('imagen', 'null')
        nacimiento = data.get('nacimiento', '')
        extension = data.get('extension', 'null')
        
        if username is None and password is None:
            response_data = {'result': 'fail', 'message':'Falta usuario y contraseña'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        if username == "null" and password == "null":
            response_data = {'result': 'fail', 'message':'Falta usuario y contraseña'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        if username is None:
            response_data = {'result': 'fail', 'message':'Falta usuario'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        if username == "null":
            response_data = {'result': 'fail', 'message':'Falta usuario'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        if password is None:
            response_data = {'result': 'fail', 'message':'Falta contraseña'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        if password == "null":
            response_data = {'result': 'fail', 'message':'Falta contraseña'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

        user_exist = User.objects.filter(username=username)
        if user_exist.count() > 0:
            response_data = {'result': 'fail', 'message':'Este usuario ya existe'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        else:
            token_existe = Tokenregister.objects.filter(token=token)
            if token_existe.count()>0:
                token_existe = Tokenregister.objects.get(token=token)
                
                if str(token_existe.userid.is_staff) == "True":
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.save()
                    tipo = tipo.lower()            
                    if imagen != "null":
                        datetime_now = str(datetime.datetime.now())
                        ruta_imagen = config.ruta_imagen_usuarios + datetime_now + "." + extension
                        ruta_imagen = ruta_imagen.replace(" ", "+")
                        ruta_imagen2 = config.ruta_imagen_konecta2 + ruta_imagen
                        ruta_imagen2 = ruta_imagen2.replace(" ", "+")
                        file = open(ruta_imagen2, "w")
                        image_b64 = imagen.replace(" ","+")
                        image_bin = base64.b64decode(image_b64)
                        file.write(image_bin)
                        file.close()
                    else:
                        ruta_imagen = config.ruta_imagen_usuarios_default    
                
                    if tipo == "profesor":
                        usuario_profesor = Profesor(idusuario=user, urlimagen=ruta_imagen, nacimiento=nacimiento, estado="Desconectado", nombre=nombre, apellido1=primer_apellido, apellido2=segundo_apellido)
                        usuario_profesor.save()
                        permisos_profesor = Permisos(idusuario=user, crear_usuario=crear_user, 
                        modificar_usuario=mod_user,eliminar_usuario=elimi_user, ver_notas=ver_nota, 
                        modificar_notas=mod_notas, ver_todos_usuarios=ver_todos_usuarios, crear_ejercicio=crear_ejercicio, 
                        modificar_ejercicio=modificar_ejercicio, eliminar_ejercicio=eliminar_ejercicio)
                        permisos_profesor.save()
                        #Si no se selecciona clase, que se mande "clases":"null"
                        if clases_array != "null":
                            for clases in clases_array:                 
                                unidad_clase = clases.get('clase')
                                id_curso = Cursos.objects.filter(idcurso=unidad_clase)
                                if id_curso.count() > 0:
                                    id_curso = Cursos.objects.get(idcurso=unidad_clase)
                                    usuario_profesor.curso.add(id_curso)
                        response_data = {'result': 'ok', 'message':'Usuario tipo profesor registrado'}
                        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

                    if tipo == "alumno":
                        usuario_alumno = Alumno(idusuario=user, urlimagen=ruta_imagen, nacimiento=nacimiento, estado="Desconectado", nombre=nombre, apellido1=primer_apellido, apellido2=segundo_apellido)
                        usuario_alumno.save()
                        #Si no se selecciona clase, que se mande "clases":"null"
                        if clases_array != "null":
                            for clases in clases_array:                 
                                unidad_clase = clases.get('clase')
                                id_curso = Cursos.objects.filter(idcurso=unidad_clase)
                                if id_curso.count() > 0:
                                    id_curso = Cursos.objects.get(idcurso=unidad_clase)
                                    usuario_alumno.curso.add(id_curso)
                        response_data = {'result': 'ok', 'message':'Usuario tipo alumno registrado'}
                        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
                    else:
                        response_data = {'result': 'fail'}
                        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

                
                buscar_permisos = Permisos.objects.get(idusuario=token_existe.userid.id)
                if buscar_permisos.crear_usuario == "true":
                    
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.save()
                    tipo = tipo.lower()            
                    if imagen != "null":
                        datetime_now = str(datetime.datetime.now())
                        ruta_imagen = config.ruta_imagen_usuarios + datetime_now + "." + extension
                        ruta_imagen = ruta_imagen.replace(" ", "+")
                        ruta_imagen2 = config.ruta_imagen_konecta2 + ruta_imagen
                        ruta_imagen2 = ruta_imagen2.replace(" ", "+")
                        file = open(ruta_imagen2, "w")
                        image_b64 = imagen.replace(" ","+")
                        image_bin = base64.b64decode(image_b64)
                        file.write(image_bin)
                        file.close()                                
                    else:
                        ruta_imagen = config.ruta_imagen_usuarios_default
                        
                    if tipo == "profesor":
                        usuario_profesor = Profesor(idusuario=user, urlimagen=ruta_imagen, nacimiento=nacimiento, estado="Desconectado", nombre=nombre, apellido1=primer_apellido, apellido2=segundo_apellido)
                        usuario_profesor.save()
                        permisos_profesor = Permisos(idusuario=user, crear_usuario=crear_user, 
                        modificar_usuario=mod_user,eliminar_usuario=elimi_user, ver_notas=ver_nota, 
                        modificar_notas=mod_notas, ver_todos_usuarios=ver_todos_usuarios, crear_ejercicio=crear_ejercicio, 
                        modificar_ejercicio=modificar_ejercicio, eliminar_ejercicio=eliminar_ejercicio)
                        permisos_profesor.save()
                        #Si no se selecciona clase, que se mande "clases":"null"
                        if clases_array != "null":
                            for clases in clases_array:					
                                unidad_clase = clases.get('clase')
                                id_curso = Cursos.objects.filter(idcurso=unidad_clase)
                                if id_curso.count() > 0:
                                    id_curso = Cursos.objects.get(idcurso=unidad_clase)
                                    usuario_profesor.curso.add(id_curso)
                        response_data = {'result': 'ok', 'message':'Usuario tipo profesor registrado'}
                        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

                    if tipo == "alumno":
                        usuario_alumno = Alumno(idusuario=user,  urlimagen=ruta_imagen, nacimiento=nacimiento, estado="Desconectado", nombre=nombre, apellido1=primer_apellido, apellido2=segundo_apellido)
                        usuario_alumno.save()
                        #Si no se selecciona clase, que se mande "clases":"null"
                        if clases_array != "null":
                            for clases in clases_array:					
                                unidad_clase = clases.get('clase')
                                id_curso = Cursos.objects.filter(idcurso=unidad_clase)
                                if id_curso.count() > 0:
                                    id_curso = Cursos.objects.get(idcurso=unidad_clase)
                                    usuario_alumno.curso.add(id_curso)
                        response_data = {'result': 'ok', 'message':'Usuario tipo alumno registrado'}
                        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
                    else:
                        response_data = {'result': 'fail'}
                        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
                else:
                    response_data = {'result': 'fail', 'message':'No tienes los permisos suficientes'}
                    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json") 
            else:
                response_data = {'result': 'fail', 'message':'Token no encontrado'}
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def invitado(request):
    """
		{
		data:
			{
			"nombre":"nombre"
			"clase":"clase"
			}
		}
    Esta vista se ejecuta cuando el usuario en el login pone "Invitado".
    En este caso se crea un usuario temporal, al cual con su nombre y caracteres aleatorios se le crea
    un nombre de usuario. A continuación se le crea su perfil de invitado, se le pone el estado como 
    conectado y a continuación se le genera un token.
    """
    random1 = id_generator()
    try:
        
        data = simplejson.loads(request.POST['data'])
        nombre = data.get('nombre', 'null')
        clase = data.get('clase', 'null')
        finish = 180
        random_user = usuario_generator()
        random_user2 = usuario_generator()
        user_name = random_user + "_" + nombre + "_" + random_user2
        user_exist = User.objects.filter(username=user_name)
        if nombre != "null":
            if user_exist.count() > 0:
                response_data = {'result': 'fail', 'message':'Este usuario ya existe'}
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
            else:
                user = User.objects.create_user(username=user_name)
                user.is_active = True
                user.save()
                usuario_invitado = Invitado(idusuario=user, nombre=nombre, estado="Conectado")
                usuario_invitado.save()
                id_curso = Cursos.objects.get(idcurso=clase)
                usuario_invitado.curso.add(id_curso)
                

                token1 = str(user.id) + "_" + random1
                tokenform = Tokenregister(token=token1, userid=user)
                tokenform.save()
                user_token = get_object_or_None(Tokenregister, userid=user)
                validity = user_token.date+datetime.timedelta(0,finish)
                response_data = {'result': 'ok', 'tipo_usuario': 'Alumno', 'token': token1, 'validity': str(validity)}
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
        else:
            response_data = {'result': 'fail', 'message':'Nombre no recibido'}
            return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def clases_profesor_usuarios(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
    Esta vista le mostrará al profesor sus clases y si tiene permisos le muestra todas las clases.
    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            cojer_usuario = Profesor.objects.get(idusuario=token_usuario.userid.id)
            tiene_permisos = Permisos.objects.get(idusuario=token_usuario.userid.id)
            response_data = {'result': 'ok', 'cursos': []}
            if tiene_permisos.ver_todos_usuarios == "true":                
                for clases in Cursos.objects.all():
                    response_data['cursos'].append({'idcurso': clases.idcurso, 'nombre': clases.nombre_curso })
            else:
                for clases in cojer_usuario.curso.all():
                    response_data['cursos'].append({'idcurso': clases.idcurso, 'nombre': clases.nombre_curso })
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}        
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def ver_usuarios(request):
    """
        {
        data:
            {
            "curso":"curso"
            "token":"token"
            }
        }
    Esta vista es para ver todos los usuarios de la base de datos.
    Para poder verlos lo primero es que hay que ser profesor. A continuación se mira si el usuario
    tiene permisos para ver todos los usuarios. Si lo tiene se le muestran todos los usuarios de la
    base de datos.
    Si no tiene estos permisos, solo se le muestran sus alumnos.
    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        curso = data.get('curso', 'null')
        existe_token = Tokenregister.objects.filter(token=token)
        if existe_token.count() > 0:
            cojer_token = Tokenregister.objects.get(token=token)
            existe_profesor = Profesor.objects.filter(idusuario=cojer_token.userid.id)
            curso_buscado = Cursos.objects.filter(nombre_curso=curso)
            if existe_profesor.count() > 0:
                cojer_profesor = Profesor.objects.get(idusuario=cojer_token.userid.id)
                tiene_permisos = Permisos.objects.get(idusuario=cojer_token.userid.id)
                if tiene_permisos.ver_todos_usuarios == "true":
                    response_data = {'result':'ok', 'profesores': [], 'alumnos': [], 'invitados': []}
                    for profesores in Profesor.objects.all():
                        response_data['profesores'].append({'id': profesores.idusuario.id, 'nombre': profesores.nombre, 'primer_apellido': profesores.apellido1, 'segundo_apellido': profesores.apellido2, 'estado': profesores.estado})
                    
                    if curso_buscado.count() > 0:
                        curso_buscado = Cursos.objects.get(nombre_curso=curso)
                        for alumnos in Alumno.objects.filter(curso=curso_buscado):
                            response_data['alumnos'].append({'id': alumnos.idusuario.id, 'nombre': alumnos.nombre, 'primer_apellido': alumnos.apellido1, 'segundo_apellido': alumnos.apellido2, 'estado': alumnos.estado})
                        for invitados in Invitado.objects.filter(curso=curso_buscado):
                            response_data['invitados'].append({'id': invitados.idusuario.id, 'nombre': invitados.nombre, 'estado': invitados.estado})
                else:
                    response_data = {'result':'ok', 'alumnos': [], 'invitados': [], 'profesores': []}
                    if curso_buscado.count() > 0:
                        curso_buscado = Cursos.objects.get(nombre_curso=curso)
                        for alumno in Alumno.objects.filter(curso=curso_buscado):
                            response_data['alumnos'].append({'id': alumno.idusuario.id, 'nombre': alumno.nombre, 'primer_apellido': alumno.apellido1, 'segundo_apellido': alumno.apellido2, 'estado': alumno.estado})
                        for invitados in Invitado.objects.filter(curso=curso_buscado):
                            response_data['invitados'].append({'id': invitados.idusuario.id, 'nombre': invitados.nombre, 'estado': invitados.estado})
            else:                
                response_data = {'result': 'fail', 'message':'El usuario no es un profesor'}
        else:
            response_data = {'result': 'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def borrar_usuario(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            }
        }
    Esta vista elimina los usuarios de los cuales se manda el id. Se elimina el usuario, su perfil, su token,
    sus permisos...
    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        idusuario = data.get('idusuario', '')

        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            cojer_token = Tokenregister.objects.get(token=token)
            buscar_permisos = Permisos.objects.get(idusuario=cojer_token.userid.id)
            if buscar_permisos.eliminar_usuario == "true":

                usuario_encontrado = User.objects.filter(id=idusuario)
                if usuario_encontrado.count()>0:
                    usuario_encontrado = User.objects.get(id=idusuario)
                    tipo1 = Alumno.objects.filter(idusuario=usuario_encontrado)
                    tipo2 = Profesor.objects.filter(idusuario=usuario_encontrado)
                    tipo3 = Invitado.objects.filter(idusuario=usuario_encontrado)
                    if tipo1.count() > 0:
                        tipo1 = Alumno.objects.get(idusuario=usuario_encontrado)
                        tipo1.curso.clear()
                        tipo1.ejercicio.clear()
                        tipo1.delete()

                    if tipo2.count() > 0:
                        tipo2 = Profesor.objects.get(idusuario=usuario_encontrado)
                        permisos_profesor = Permisos.objects.filter(idusuario=usuario_encontrado)
                        if permisos_profesor.count()>0:
                            permisos_profesor = Permisos.objects.get(idusuario=usuario_encontrado)
                            permisos_profesor.delete()
                        tipo2.curso.clear()
                        tipo2.delete()

                    if tipo3.count() > 0:
                        tipo3 = Invitado.objects.get(idusuario=usuario_encontrado)
                        tipo3.curso.clear()
                        tipo3.ejercicio.clear()
                        tipo3.delete()
                    token_usuario = Tokenregister.objects.filter(userid=usuario_encontrado)
                    if token_usuario.count()>0:
                        token_usuario = Tokenregister.objects.get(userid=usuario_encontrado)
                        token_usuario.delete()
                    usuario_encontrado.delete()

                    response_data = {'result': 'ok'}
                else:
                    response_data = {'result': 'fail', 'message': 'No existe el usuario'}
            else:
                response_data = {'result': 'fail', 'message': 'No tienes permisos para realizar la operacion'}
        else:
            response_data = {'result': 'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
@csrf_exempt
def modificar_usuario(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            "nombre":"nombre"
            "primer_apellido":"primer_apellido"
            "segundo_apellido":"segundo_apellido"
            "username":"username"
            "clases":[{"clase":"clase"}]
            "crear_usuario":"crear_usuario"
            "modificar_usuario":"modificar_usuario"
            "eliminar_usuario":"eliminar_usuario"
            "ver_nota":"ver_nota"
            "modificar_notas":"modificar_notas"
            "ver_todos_usuarios":"ver_todos_usuarios"

            }
        }
    Esta vista modifica los usuarios.
    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        idusuario = data.get('idusuario', '')
        nombre = data.get('nombre', '')
        apellido1 = data.get('primer_apellido', '')
        apellido2 = data.get('segundo_apellido', '')
        username = data.get('username', '')
        clases_array = data.get('clases', '')


        crear_user = data.get('crear_usuario', 'false')
        mod_user = data.get('modificar_usuario', 'false')
        elimi_user = data.get('eliminar_usuario', 'false')
        ver_nota = data.get('ver_notas', 'false')
        mod_notas = data.get('modificar_notas', 'false')
        ver_todos_usuarios = data.get('ver_todos_usuarios', 'false')
        crear_ejercicio = data.get('crear_ejercicios', 'false')
        modificar_ejercicio = data.get('modificar_ejercicios', 'false')
        eliminar_ejercicio = data.get('eliminar_ejercicios', 'false')

        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            cojer_token = Tokenregister.objects.get(token=token)
            buscar_permisos = Permisos.objects.get(idusuario=cojer_token.userid.id)
            if buscar_permisos.modificar_usuario == "true":
                usuario_encontrado = User.objects.filter(id=idusuario)
                if usuario_encontrado.count()>0:
                    usuario_encontrado = User.objects.get(id=idusuario)
                    usuario_encontrado.username = username
                    usuario_encontrado.save()

                    tipo1 = Alumno.objects.filter(idusuario=usuario_encontrado)
                    tipo2 = Profesor.objects.filter(idusuario=usuario_encontrado)
                    tipo3 = Invitado.objects.filter(idusuario=usuario_encontrado)
                    if tipo1.count() > 0:
                        tipo1 = Alumno.objects.get(idusuario=usuario_encontrado)
                        tipo1.nombre = nombre
                        tipo1.apellido1 = apellido1
                        tipo1.apellido2 = apellido2
                        tipo1.save()
                        tipo1.curso.clear()
                        for clases in clases_array:                 
                                unidad_clase = clases.get('clase')
                                id_curso = Cursos.objects.filter(idcurso=unidad_clase)
                                if id_curso.count() > 0:
                                    id_curso = Cursos.objects.get(idcurso=unidad_clase)
                                    tipo1.curso.add(id_curso)


                    if tipo2.count() > 0:
                        tipo2 = Profesor.objects.get(idusuario=usuario_encontrado)
                        permisos_profesor = Permisos.objects.filter(idusuario=usuario_encontrado)
                        if permisos_profesor.count()>0:
                            permisos_profesor = Permisos.objects.get(idusuario=usuario_encontrado)
                            permisos_profesor.crear_usuario = crear_user
                            permisos_profesor.ver_todos_usuarios = ver_todos_usuarios
                            permisos_profesor.modificar_usuario = mod_user
                            permisos_profesor.eliminar_usuario = elimi_user
                            permisos_profesor.ver_notas = ver_nota
                            permisos_profesor.modificar_notas = mod_notas
                            permisos_profesor.crear_ejercicio = crear_ejercicio
                            permisos_profesor.modificar_ejercicio = modificar_ejercicio
                            permisos_profesor.eliminar_ejercicio = eliminar_ejercicio
                            permisos_profesor.save()
                        tipo2.nombre = nombre
                        tipo2.apellido1 = apellido1
                        tipo2.apellido2 = apellido2
                        tipo2.save()
                        for clases in clases_array:                 
                                unidad_clase = clases.get('clase')
                                id_curso = Cursos.objects.filter(idcurso=unidad_clase)
                                if id_curso.count() > 0:
                                    id_curso = Cursos.objects.get(idcurso=unidad_clase)
                                    tipo2.curso.add(id_curso)                        

                    if tipo3.count() > 0:
                        tipo3 = Invitado.objects.get(idusuario=usuario_encontrado)
                        tipo3.nombre = nombre
                        tipo3.save()
                        for clases in clases_array:                 
                                unidad_clase = clases.get('clase')
                                id_curso = Cursos.objects.filter(idcurso=unidad_clase)
                                if id_curso.count() > 0:
                                    id_curso = Cursos.objects.get(idcurso=unidad_clase)
                                    tipo3.curso.add(id_curso)                     

                    response_data = {'result': 'ok'}
                else:
                    response_data = {'result': 'fail', 'message': 'No existe el usuario'}
            else:
                response_data = {'result': 'fail', 'message': 'No tienes permisos para realizar la operacion'}
        else:
            response_data = {'result': 'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


@csrf_exempt
def crear_notificacion(request):
    """
        {
        data:
            {
            "token":"token"
            "iddestino":"idddestino"
            "tipo":"tipo"
            "mensaje":"mensaje"
            }
        }

    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        iddestino = data.get('iddestino', '')
        tipo = data.get('tipo', '')
        mensaje = data.get('mensaje', '')
        finish = 604800
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            usuario_existe = User.objects.filter(id=iddestino)
            if usuario_existe.count() > 0:
                usuario_existe = User.objects.get(id=iddestino)
                fecha_expiracion = datetime.datetime.now(pytz.utc)+datetime.timedelta(0,finish)
                guardar_notificacion = Notificacion(idusuario=usuario_existe, date=fecha_expiracion, tipo=tipo, mensaje=mensaje)
                guardar_notificacion.save()
                response_data = {'result':'ok', 'message':'Notificacion creada'}
            else:
                response_data = {'result':'fail', 'message':'Usuario no encontrado'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def consultar_notificacion(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }

    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            token_existe = Tokenregister.objects.get(token=token)
            notificaciones_total = Notificacion.objects.filter(idusuario=token_existe.userid.id)
            response_data = {'result':'ok', 'notificaciones':[]}
            for notificacion_individual in notificaciones_total:
                response_data['notificaciones'].append({'idnotificacion': notificacion_individual.idnotificacion, 'tipo':notificacion_individual.tipo, 'mensaje':notificacion_individual.mensaje})
                if notificacion_individual.date < datetime.datetime.now(pytz.utc):
                    notificacion_individual.delete()
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def borrar_notificacion(request):
    """
        {
        data:
            {
            "token":"token"
            "idnotificacion":"idnotificacion"
            }
        }

    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        idnotificacion = data.get('idnotificacion', '')
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            token_existe = Tokenregister.objects.get(token=token)
            notificaciones_total = Notificacion.objects.filter(idusuario=token_existe.userid.id, idnotificacion=idnotificacion)
            if notificaciones_total.count() > 0:
                notificaciones_total = Notificacion.objects.get(idusuario=token_existe.userid.id, idnotificacion=idnotificacion)
                notificaciones_total.delete()
                response_data = {'result':'ok', 'message':'Notificacion eliminada'}
            else:
                response_data = {'result':'fail', 'message':'Notificacion no encontrada'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def comprobar_pass(request):
    """
        {
        data:
            {
            "token":"token"
            "password":"password"
            }
        }

    """
    try:
        
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        password = data.get('password', '')

        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            token_existe = Tokenregister.objects.get(token=token)
            usuario_existe = User.objects.filter(id=token_existe.userid.id)
            if usuario_existe.count() > 0:
                usuario_existe = User.objects.get(id=token_existe.userid.id)
                if usuario_existe.password == password:
                    response_data = {'result':'ok'}
                else:
                    response_data = {'result':'fail', 'message':'Password erronea'}
            else:
                response_data = {'result':'fail', 'message':'Usuario no encontrado'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def reiniciar_password(request):
    """
        {
        data:
            {
            "token":"token"
            "password":"password"
            }
        }

    """
    try:
        
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')
        password = data.get('password', '')

        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            token_existe = Tokenregister.objects.get(token=token)
            usuario_existe = User.objects.filter(id=token_existe.userid.id)
            if usuario_existe.count() > 0:
                usuario_existe = User.objects.get(id=token_existe.userid.id)
                usuario_existe.set_password(password)
                usuario_existe.save()
                response_data = {'result':'ok', 'message':'Contraseña cambiada'}
            else:
                response_data = {'result':'fail', 'message':'Usuario no encontrado'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def comprobar_token(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
    Comprueba si el token existe.
    """
    try:
        
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', '')

        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            response_data = {'result': 'ok'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def reset_password(request):
    """
        {
        data:
            {
            "token":"token"
            "id":"id"
            "password":"password"
            }
        }
        Cambia la password
    """
    try:
        data = simplejson.loads(request.POST['data'])
        idusuario = data.get('idusuario', '')
        password = data.get('password', '')
        token = data.get('token', '')
        
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            paco = User.objects.get(id=idusuario)
            paco.set_password(password)
            paco.save()
            response_data = {'result': 'ok'}
        else:
            response_data = {'result': 'fail'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

