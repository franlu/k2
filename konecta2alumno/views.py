#-*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.template import RequestContext

from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.conf import settings
from konecta2app.models import Permisos, MateriasEjercicios, EjerciciosPendientes, Corregir, Dificultad, Notificacion, CursosEjercicios, Tokenregister, Cursos, Profesor, Alumno, Invitado, Ejercicios
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
from annoying.functions import get_object_or_None

@csrf_exempt
def todas_clases(request):
    """
    Solo llamar a esta vista y devuelve todas las cases disponibles en el instituto de la base de datos.
    """
    try:
    	response_data = {'clases': [], 'result': 'ok'}
        for cursos in Cursos.objects.all():
            response_data['clases'].append({'id': cursos.idcurso, 'nombre': cursos.nombre_curso})
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def ejercicios_pendientes(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        Esta vista muestra al usuario que envia el token, los ejercicios pendientes por hacer que tiene.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            comprobar_ejercicios = EjerciciosPendientes.objects.filter(idalumno=token_usuario.userid.id)
            if comprobar_ejercicios.count() > 0:
                response_data = {'result': 'ok', 'ejercicios': []}
                for ejercicios in EjerciciosPendientes.objects.filter(idalumno=token_usuario.userid.id):
                    obtener_ejercicio = Ejercicios.objects.filter(idejercicio=ejercicios.idejercicio.idejercicio)
                    if obtener_ejercicio.count() > 0:
                        obtener_ejercicio = Ejercicios.objects.get(idejercicio=ejercicios.idejercicio.idejercicio)
                        response_data['ejercicios'].append({'fecha': ejercicios.fecha, 'idcorregir':ejercicios.idcorregir.idcorregir,'idprofesor': ejercicios.idprofesor.idusuario.id, 'titulo': obtener_ejercicio.titulo, 'consejo': obtener_ejercicio.consejo,'descripcion': obtener_ejercicio.descripcion, 'imagen': obtener_ejercicio.imagen, 'dificultad': obtener_ejercicio.dificultad.nombre, 'idejercicio': obtener_ejercicio.idejercicio, 'tipo': obtener_ejercicio.tipo, 'interfaz': obtener_ejercicio.interfaz, 'calculadora': obtener_ejercicio.calculadora, 'materia': obtener_ejercicio.materia.nombre, 'idmateria': obtener_ejercicio.materia.idmateria})
            else:
                response_data = {'result':'fail', 'message':'Ejercicio no encontrado'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def detalles_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idejercicio":"idejercicio"
            }
        }
        Esta vista le manda al usuario los detalles del ejercicio del cual ha enviado el id.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            comprobar_usuario = Alumno.objects.filter(idusuario=token_usuario.userid.id)
            if comprobar_usuario.count() > 0:
                comprobar_ejercicio = Ejercicios.objects.filter(idejercicio=idejercicio)
                if comprobar_ejercicio.count() > 0:
                    obtener_ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                    obtener_corregir = Corregir.objects.get(idusuario=token_usuario.userid.id,idejercicio=idejercicio)
                    response_data = {'result': 'ok', 'titulo': obtener_ejercicio.titulo, 'idcorregir':obtener_corregir.idcorregir,'descripcion': obtener_ejercicio.descripcion, 'idejercicio': obtener_ejercicio.idejercicio, 'imagen': obtener_ejercicio.imagen, 'calculadora': obtener_ejercicio.calculadora, 'dificultad': obtener_ejercicio.dificultad.nombre, 'interfaz':  obtener_ejercicio.interfaz, 'consejo': obtener_ejercicio.consejo}
                else:
                    response_data = {'result':'fail', 'message': 'Ejercicio no encontrado'}
            else:
                response_data = {'result': 'fail', 'message': 'Alumno no encontrado'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

