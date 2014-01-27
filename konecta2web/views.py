# -*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.conf import settings
from konecta2app.models import Permisos, MateriasEjercicios, Incidencias, Notificacion, CursosEjercicios, EjerciciosPendientes
from konecta2app.models import Tema, Tokenregister, Cursos, Observaciones, Profesor, Alumno, Invitado, Ejercicios, Dificultad, Corregir
from konecta2app.models import EjerciciosClase, Controles, Examenes, Globales
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
import urllib2
"""
Método que envia a una url una peticion con un json
"""
@csrf_exempt
def envio(request):
    response_data = {'result':'ok'}
    result = urllib2.urlopen('http://192.168.1.127:8001/prueba/', simplejson.dumps(response_data))
    content = result.read()    
    jsonyasiquesi = json.loads(content)
    response_data = {'result': jsonyasiquesi.get('result')}
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

"""
Método que recibe la peticion y devu
"""

@csrf_exempt
def recibir(request):
    objs = json.loads(request.raw_post_data)
    objs.get('result')
    response_data = {'result':'ok'}
    return HttpResponse(simplejson.dumps(response_data),mimetype="applicaion/json")


@csrf_exempt
def login_web(request):
    try:
        objs = json.loads(request.raw_post_data)    
        username = objs.get('username')
        password = objs.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response_data = {'result':'ok'}
        else:
            response_data = {'result':'fail'}
        return HttpResponse(simplejson.dumps(response_data),mimetype="applicaion/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def logout_web(request):
    try:
        auth.logout(request)
        response_data = {'result':'ok'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def datos_alumno_web(request):
    try:
        if request.user.is_authenticated():
            datos_alumno = Alumno.objects.filter(idusuario=request.user.id)
            if datos_alumno.count() > 0:
                datos_alumno = Alumno.objects.get(idusuario=request.user.id)
                response_data = {'result':'ok', 'nombre': datos_alumno.nombre, 'apellido1': datos_alumno.apellido1,
                                 'apellido2': datos_alumno.apellido2, 'estado': datos_alumno.estado, 'nacimiento': datos_alumno.nacimiento}  
            else:
                response_data = {'result':'fail', 'mensaje': 'El alumno no existe'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def incidencias_web(request):
    try:
        if request.user.is_authenticated():
            incidencia = Incidencias.objects.filter(idusuario=request.user.id)
            if incidencia.count() > 0:
                incidencia = Incidencias.objects.get(idusuario=request.user.id)
                response_data = {'result':'ok', 'incidencia': incidencia.comentario}
            else:
                response_data = {'result':'ok', 'incidencia': 'No hay incidencias para este usuario'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def observaciones_web(request):
    try:
        if request.user.is_authenticated():
            observacion = Observaciones.objects.filter(idusuario=request.user.id)
            if observacion.count() > 0:
                observacion = Observaciones.objects.get(idusuario=request.user.id)
                response_data = {'result':'ok', 'observacion': observacion.comentario}
            else:
                response_data = {'result':'ok', 'observacion': 'No hay observaciones para este usuario'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def ejercicios_pendientes_web(request):
    try:
        if request.user.is_authenticated():
            ejercicios = EjerciciosPendientes.objects.filter(idusuario=request.user.id)
            if ejercicios.count() > 0:
                response_data = {'result':'ok', 'ejercicio': []}
                for ejercicio in ejercicios:
                    datos_ejercicio = Ejercicios.objects.filter(idejercicio=ejercicio.idejercicio.idejercicio)
                    if datos_ejercicio.count() > 0:
                        datos_ejercicio = Ejercicios.objects.get(idejercicio=ejercicio.idejercicio.idejercicio)
                        response_data['ejercicio'].append({'titulo': datos_ejercicio.titulo, 'materia': datos_ejercicio.materia.nombre, 'fecha': ejercicio.fecha})                
            else:
                response_data = {'result':'fail', 'mensaje': 'No hay ejercicios'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def ejercicios_clase_web(request):
    try:
        if request.user.is_authenticated():
            ejercicios = EjerciciosClase.objects.filter(idusuario=request.user.id)
            if ejercicios.count() > 0:
                response_data = {'result':'ok', 'ejercicio': []}
                for ejercicio in ejercicios:
                    datos_ejercicio = Ejercicios.objects.filter(idejercicio=ejercicio.idejercicio.idejercicio)
                    if datos_ejercicio.count() > 0:
                        datos_ejercicio = Ejercicios.objects.get(idejercicio=ejercicio.idejercicio.idejercicio)
                        response_data['ejercicio'].append({'titulo': datos_ejercicio.titulo, 'materia': datos_ejercicio.materia.nombre, 'fecha': ejercicio.fecha, 'nota': ejercicios.nota,
                                                           'booleano': ejercicio.booleano, 'resultado': ejercicio.resultado, 'tiempo_realizacion': ejercicio.tiempo_realizacion, 'intentos': ejercicio.intentos})                
            else:
                response_data = {'result':'fail', 'mensaje': 'No hay ejercicios'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def controles_web(request):
    try:
        if request.user.is_authenticated():
            ejercicios = Controles.objects.filter(idusuario=request.user.id)
            if ejercicios.count() > 0:
                response_data = {'result':'ok', 'ejercicio': []}
                for ejercicio in ejercicios:
                    datos_ejercicio = Ejercicios.objects.filter(idejercicio=ejercicio.idejercicio.idejercicio)
                    if datos_ejercicio.count() > 0:
                        datos_ejercicio = Ejercicios.objects.get(idejercicio=ejercicio.idejercicio.idejercicio)
                        response_data['ejercicio'].append({'titulo': datos_ejercicio.titulo, 'materia': datos_ejercicio.materia.nombre, 'fecha': ejercicio.fecha, 'nota': ejercicios.nota,
                                                           'booleano': ejercicio.booleano, 'resultado': ejercicio.resultado, 'tiempo_realizacion': ejercicio.tiempo_realizacion, 'intentos': ejercicio.intentos})                
            else:
                response_data = {'result':'fail', 'mensaje': 'No hay ejercicios'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def examenes_web(request):
    try:
        if request.user.is_authenticated():
            ejercicios = Examenes.objects.filter(idusuario=request.user.id)
            if ejercicios.count() > 0:
                response_data = {'result':'ok', 'ejercicio': []}
                for ejercicio in ejercicios:
                    datos_ejercicio = Ejercicios.objects.filter(idejercicio=ejercicio.idejercicio.idejercicio)
                    if datos_ejercicio.count() > 0:
                        datos_ejercicio = Ejercicios.objects.get(idejercicio=ejercicio.idejercicio.idejercicio)
                        response_data['ejercicio'].append({'titulo': datos_ejercicio.titulo, 'materia': datos_ejercicio.materia.nombre, 'fecha': ejercicio.fecha, 'nota': ejercicios.nota,
                                                           'booleano': ejercicio.booleano, 'resultado': ejercicio.resultado, 'tiempo_realizacion': ejercicio.tiempo_realizacion, 'intentos': ejercicio.intentos})                
            else:
                response_data = {'result':'fail', 'mensaje': 'No hay ejercicios'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

@csrf_exempt
def globales_web(request):
    try:
        if request.user.is_authenticated():
            ejercicios = Globales.objects.filter(idusuario=request.user.id)
            if ejercicios.count() > 0:
                response_data = {'result':'ok', 'ejercicio': []}
                for ejercicio in ejercicios:
                    datos_ejercicio = Ejercicios.objects.filter(idejercicio=ejercicio.idejercicio.idejercicio)
                    if datos_ejercicio.count() > 0:
                        datos_ejercicio = Ejercicios.objects.get(idejercicio=ejercicio.idejercicio.idejercicio)
                        response_data['ejercicio'].append({'titulo': datos_ejercicio.titulo, 'materia': datos_ejercicio.materia.nombre, 'fecha': ejercicio.fecha, 'nota': ejercicios.nota,
                                                           'booleano': ejercicio.booleano, 'resultado': ejercicio.resultado, 'tiempo_realizacion': ejercicio.tiempo_realizacion, 'intentos': ejercicio.intentos})                
            else:
                response_data = {'result':'fail', 'mensaje': 'No hay ejercicios'}
        else:
            response_data = {'result':'fail', 'mensaje':'No estás conectado'}
                      
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")