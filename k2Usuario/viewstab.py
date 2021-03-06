# -*- coding: utf-8 -*-
import django.contrib.auth as auth
import django.http as http

from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from k2Usuario.models import Alumno, Profesor,Clase, Tokenregister
from k2utils.token import id_generator

import datetime
import json
import pytz


@csrf_exempt
def login(request):

    """
    {
        "data":{
            username:"<username>",
            password:"<password>"
            lugar:"<lugar>",



        }
    }
    Con el usuario y el password, hace un inicio de sesión de los usuarios poniendole el estado en Conectado.
    A continuación les crea un token y si ya tenian uno, cambian el anterior por otro nuevo.
    En caso de mandar un usuario o password que no exista da un error.
    """
    random1 = id_generator()
    userlog = []
    try:
        userlog = json.loads(request.POST['data'])
        username = userlog.get('username').lower()
        password = userlog.get('password')
        lugar = userlog.get('lugar','null')
        type_user = userlog.get('type')
        user = auth.authenticate(username=username, password=password)
        finish = 1

        if username is None and password is None:
            response_data = {'result': 'fail', 'message': 'Falta el username y el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if username is None:
            response_data = {'result': 'fail', 'message': 'Falta el username'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None:
            response_data = {'result': 'fail', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                usuario = User.objects.get(username=user.username)
                tipo1 = Alumno.objects.filter(idusuario=usuario)
                tipo2 = Profesor.objects.filter(idusuario=usuario)
                user_token = get_object_or_None(Tokenregister, userid=usuario)
                if user_token==None:
                    token1 = str(user.id) + "_" + random1
                    tokenform = Tokenregister(token=token1, userid=usuario)
                    tokenform.save()
                    user_token = get_object_or_None(Tokenregister, userid=usuario)
                else:
                    if user_token.date+datetime.timedelta(0,finish) < datetime.datetime.now(pytz.utc):
                       user_token.date = datetime.datetime.now(pytz.utc)
                       user_token.token = str(usuario.id) + "_" + random1
                       user_token.save()
                validity = user_token.date+datetime.timedelta(0,finish)
                #response_data = {'result': 'ok', 'token': user_token.token, 'tipo_usuario': 'Profesor', 'validity': str(validity)}
                #return http.HttpResponse(json.dumps(response_data), content_type="application/json")
                if tipo1.count() > 0:
                    tipo1 = Alumno.objects.get(idusuario=usuario)
                    tipo1.estado = "Conectado"
                    tipo1.save()
                    tipo_usuario = "Alumno"
                else:
                    if tipo2.count() > 0:
                        tipo2 = Profesor.objects.get(idusuario=usuario)
                        tipo2.estado = "Conectado"
                        tipo2.save()
                        tipo_usuario = "Profesor"
                    else:
                        tipo_usuario="Desconocido"

                response_data = {'result': 'ok', 'token': user_token.token, 'validity': str(validity), 'tipo_usuario':tipo_usuario,}
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                response_data = {'result': 'fail', 'message': 'Usuario no activado.'}
                return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        else:
            response_data = {'result': 'fail', 'message': 'Usuario no válido.'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def logout(request):
    """
    {
        data:{
            token:"<token>",
            lugar:"<lugar>"
        }
    }
    Con el token busca el usuario y con este mira si es tipo profesor, alumno o invitado.
    Si es profesor o alumno, le pone el estado en desconectado y elimina el token.
    Hardcode: En caso de que el usuario sea invitado, borra el usuario, y su token.
    """
    data = []
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', '')
        lugar = data.get('lugar', '')
        tr = Tokenregister.objects.filter(token=token)
        if tr.count() > 0:
            user_token = Tokenregister.objects.get(token=token)
            usuario_encontrado = User.objects.get(id=user_token.userid.id)
            tipo1 = Alumno.objects.filter(idusuario=usuario_encontrado)
            tipo2 = Profesor.objects.filter(idusuario=usuario_encontrado)
            #tipo3 = Invitado.objects.filter(idusuario=usuario_encontrado)
            if tipo1.count() > 0:
                tipo1 = Alumno.objects.get(idusuario=usuario_encontrado)
                tipo1.estado = "Desconectado"
                tipo1.save()
            else:
                if tipo2.count() > 0:
                    tipo2 = Profesor.objects.get(idusuario=usuario_encontrado)
                    tipo2.estado = "Desconectado"
                    tipo2.save()
                """else:
                    if tipo3.count() > 0:
                        tipo3 = Invitado.objects.get(idusuario=usuario_encontrado)
                        tipo3.curso.clear()
                        tipo3.ejercicio.clear()
                        usuario_encontrado.delete()
                        tipo3.delete()
                    """
            user_token.delete()
            response_data = {'result': 'ok', 'message':'Logout'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data = {'result': 'fail', 'message':'Token no encontrado'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def clases_profesor(request):
    """
		{
		data:
			{
			"token":"token"
			}
		}
    Esta vista le mostrará al profesor sus clases cuando se logea y abre la ventala donde ve los alumnos.
    """

    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            cojer_usuario = Profesor.objects.get(idusuario=token_usuario.userid.id)
            response_data = {'result': 'ok', 'clases_profesor': []}
            for clases in cojer_usuario.clases.all():
                response_data['clases_profesor'].append({'idclase': clases.id, 'nombre': clases.nombre })
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def alumnos_por_clase(request):
    """
		{
		data:
			{
			"token":"token"
			"idclase":"idclase"
			}
		}
    Esta vista es para que el profesor pueda ver todos los alumnos tanto conectados como desconectados, como
    invitados.
    """
    data = []
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idclase = data.get('idclase', 'null')
        usuario_existe = Tokenregister.objects.filter(token=token)

        if usuario_existe.count() > 0:
            response_data = {'result': 'ok', 'alumnos_registrados':[]}
            clase_buscada = Clase.objects.get(id=idclase)
            alumnos_clase = Alumno.objects.filter(clase=clase_buscada)
            #invitados_clase = Invitado.objects.filter(curso=clase_buscada)

            #if invitados_clase.count() > 0:
                #for invitados_unidad in invitados_clase:
                    #response_data['alumnos_registrados'].append({'clase':clase_buscada.nombre_curso, 'nombre': invitados_unidad.nombre, 'estado': 'Invitado', 'id': invitados_unidad.idusuario.id})
            if alumnos_clase.count() > 0:
                for alumnos_unidad in alumnos_clase:
                    response_data['alumnos_registrados'].append({'clase':clase_buscada.nombre, 'nombre': alumnos_unidad.nombre, 'estado': alumnos_unidad.estado, 'id': alumnos_unidad.idusuario.id})

        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")