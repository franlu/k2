#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.conf import settings
from konecta2app.models import Permisos, MateriasEjercicios, Incidencias, Notificacion, CursosEjercicios
from konecta2app.models import Tema, Tokenregister, Cursos, Observaciones, Profesor, Alumno, Invitado, Ejercicios, Dificultad, Corregir
from konecta2app.models import EjerciciosClase, Globales, Examenes, Controles
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




@csrf_exempt
def guardar_nota(request):
    """
        {
        data:
            {
            "token":"token"
            "idejercicio":"idejercicio"
            "fecha":"fecha"
            "idusuario":"idusuario"
            "idclase":"idclase"
            "nota":"nota"
            "bien_mal":"bien_mal"
            "tiempo_realizacion":"tiempo_realizacion"
            "resultado":"resultado"
            "imagen":"imagen"
            "intentos":"intentos"
            Segun el tipo de ejercicio que se envia se guarda el resultado del ejercicio en una tabla u otra

            }
        }
    
    """
    data = []
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        fecha = datetime.datetime.now(pytz.utc)+datetime.timedelta(0,7200)
        fecha = str(fecha)
        idusuario = data.get('idusuario', 'null')
        clase = data.get('idclase', 'null')
        nota = data.get('nota', 'null')
        booleano = data.get('bien_mal', 'null')
        tiempo_realizacion = data.get('tiempo_realizacion', 'null')
        resultado = data.get('resultado', '')
        imagen = data.get('imagen')
        imagen_b64 = data.get('imagen_64','null')
        intentos = data.get('intentos')
        
        if imagen_b64 != "null":
            file = open(config.ruta_imagen_konecta2+imagen, "rw+")
            imagen_b64 = imagen_b64.replace(" ","+")
            image_bin = base64.b64decode(imagen_b64)
            file.write(image_bin)
            file.close()

        usuario_existe = Tokenregister.objects.filter(token=token)
        if usuario_existe.count() > 0:
            usuario_existe = Tokenregister.objects.get(token=token)
            ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
            usuario = User.objects.get(id=idusuario)
            profesor_id = User.objects.get(id=usuario_existe.userid.id)
            idprofesor = Profesor.objects.get(idusuario=profesor_id)
            idclase = Cursos.objects.get(idcurso=clase)
                   
            if ejercicio.tipo == '0':
                guardar_datos = EjerciciosClase(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                guardar_datos.save()
                response_data = {'result':'ok'}
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

            if ejercicio.tipo == '3':
                guardar_datos = Globales(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                guardar_datos.save()
                response_data = {'result':'ok'}
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

            if ejercicio.tipo == '2':
                guardar_datos = Examenes(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                guardar_datos.save()
                response_data = {'result':'ok'}
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

            if ejercicio.tipo == '1':
                guardar_datos = Controles(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                guardar_datos.save()
                response_data = {'result':'ok'}
                return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

            else:
                response_data = {'result':'fail', 'message':'No se ha podido guardar, tipo no encontrado'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}           
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def guardar_nota_array(request):
    """
        {
        data:
            {
            "token":"token"
            "array":[{            
                "idejercicio":"idejercicio"
                "fecha":"fecha"
                "idusuario":"idusuario"
                "idclase":"idclase"
                "nota":"nota"
                "bien_mal":"bien_mal"
                "tiempo_realizacion":"tiempo_realizacion"
                "resultado":"resultado"
                "imagen":"imagen"
                "intentos":"intentos"

            }]
            }
        }
        Segun el tipo de ejercicio que se envia se guarda el resultado del ejercicio en una tabla u otra

    """
    data = []
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        array = data.get('array')         
        usuario_existe = Tokenregister.objects.filter(token=token)
        if usuario_existe.count() > 0:
            usuario_existe = Tokenregister.objects.get(token=token)
            profesor_id = User.objects.get(id=usuario_existe.userid.id)
            idprofesor = Profesor.objects.get(idusuario=profesor_id)
            
            for array_individual in array:
                
                idejercicio = array_individual.get('idejercicio', 'null')
                fecha = datetime.datetime.now(pytz.utc)+datetime.timedelta(0,7200)
                fecha = str(fecha)
                idusuario = array_individual.get('idusuario', 'null')
                clase = array_individual.get('idclase', 'null')
                nota = array_individual.get('nota', 'null')
                booleano = array_individual.get('bien_mal', 'null')
                tiempo_realizacion = array_individual.get('tiempo_realizacion', 'null')
                resultado = array_individual.get('resultado', '')
                imagen = array_individual.get('imagen')
                intentos = array_individual.get('intentos')
                
                ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                usuario = User.objects.get(id=idusuario)
                
                idclase = Cursos.objects.get(idcurso=clase)
                       
                if ejercicio.tipo == '0':
                    guardar_datos = EjerciciosClase(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                    idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                    guardar_datos.save()    
                if ejercicio.tipo == '3':
                    guardar_datos = Globales(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                    idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                    guardar_datos.save()    
                if ejercicio.tipo == '2':
                    guardar_datos = Examenes(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                    idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                    guardar_datos.save()    
                if ejercicio.tipo == '1':
                    guardar_datos = Controles(imagen=imagen, intentos=intentos, idejercicio=ejercicio, fecha=fecha, idusuario=usuario, idprofesor=idprofesor, resultado=resultado,
                                                    idclase=idclase, nota=nota, booleano=booleano, tiemporealizacion=tiempo_realizacion)
                    guardar_datos.save()        
            response_data = {'result':'ok'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}           
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def ver_notas(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            "idmateria":"idmateria"
            "tipo":"tipo"
            }
        }
    
    """
    data = []
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        idmateria = data.get('idmateria', '')
        tipo = data.get('tipo', '')
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            response_data = {'result':'ok', 'clase':[], 'examenes':[], 'globales':[], 'controles':[]}
            usuario_existe = User.objects.filter(id=idusuario)
            if usuario_existe.count() > 0:       
                if tipo == 0:         
                    for ejercicios_clase in EjerciciosClase.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=ejercicios_clase.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=ejercicios_clase.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['clase'].append({'titulo': ejercicio_existe.titulo, 'nota':ejercicios_clase.nota, 'nota_booleana': ejercicios_clase.booleano, 'fecha': ejercicios_clase.fecha})
                if tipo == 3:         
                    for ejercicios_global in Globales.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=ejercicios_global.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=ejercicios_global.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['globales'].append({'titulo': ejercicio_existe.titulo, 'nota':ejercicios_global.nota, 'nota_booleana': ejercicios_global.booleano, 'fecha': ejercicios_global.fecha})
                if tipo == 1:         
                    for control in Controles.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=control.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=control.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['controles'].append({'titulo': ejercicio_existe.titulo, 'nota':control.nota, 'nota_booleana': control.booleano, 'fecha': control.fecha})
                if tipo == 2:         
                    for examen in Examenes.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=examen.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=examen.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['examenes'].append({'titulo': ejercicio_existe.titulo, 'nota':examen.nota, 'nota_booleana': examen.booleano, 'fecha': examen.fecha})

            else:
                response_data = {'result':'fail', 'message':'No se ha encontrado el usuario'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}           
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def ver_notas_detallado(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            "idmateria":"idmateria"
            "tipo":"tipo"
            }
        }
    
    """
    data = []
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        idmateria = data.get('idmateria', '')
        tipo = data.get('tipo', '')
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            response_data = {'result':'ok', 'clase':[], 'examenes':[], 'globales':[], 'controles':[]}
            usuario_existe = User.objects.filter(id=idusuario)
            if usuario_existe.count() > 0:       
                if tipo == 0:         
                    for ejercicios_clase in EjerciciosClase.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=ejercicios_clase.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=ejercicios_clase.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['clase'].append({'titulo': ejercicio_existe.titulo, 'descripcion': ejercicio_existe.descripcion,
                                                               'clase': ejercicios_clase.idclase.nombre_curso ,'imagen': ejercicios_clase.imagen,
                                                               'resultado': ejercicios_clase.resultado, 'tiempo_realizacion': ejercicios_clase.tiemporealizacion, 
                                                               'intentos': ejercicios_clase.intentos, 'nota':ejercicios_clase.nota, 
                                                               'bien_mal': ejercicios_clase.booleano, 'fecha': ejercicios_clase.fecha})
                if tipo == 3:         
                    for ejercicios_global in Globales.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=ejercicios_global.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=ejercicios_global.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['globales'].append({'titulo': ejercicio_existe.titulo, 'descripcion': ejercicio_existe.descripcion ,
                                                                  'clase': ejercicios_global.idclase.nombre_curso ,'imagen': ejercicios_global.imagen,
                                                                  'resultado': ejercicios_global.resultado, 'tiempo_realizacion': ejercicios_global.tiemporealizacion, 
                                                                  'intentos': ejercicios_global.intentos,'nota':ejercicios_global.nota, 
                                                                  'bien_mal': ejercicios_global.booleano, 'fecha': ejercicios_global.fecha})
                if tipo == 1:         
                    for control in Controles.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=control.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=control.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['controles'].append({'titulo': ejercicio_existe.titulo, 'descripcion': ejercicio_existe.descripcion,
                                                                   'clase': control.idclase.nombre_curso ,'imagen': control.imagen,
                                                                   'resultado': control.resultado, 'tiempo_realizacion': control.tiemporealizacion, 
                                                                   'intentos': control.intentos,'nota':control.nota, 
                                                                   'bien_mal': control.booleano, 'fecha': control.fecha})
                if tipo == 2:         
                    for examen in Examenes.objects.filter(idusuario=idusuario):
                        ejercicio_existe = Ejercicios.objects.filter(idejercicio=examen.idejercicio.idejercicio)
                        if ejercicio_existe.count() > 0:
                            ejercicio_existe = Ejercicios.objects.get(idejercicio=examen.idejercicio.idejercicio)
                            if str(ejercicio_existe.materia.idmateria) == str(idmateria):                             
                                response_data['examenes'].append({'titulo': ejercicio_existe.titulo, 'descripcion': ejercicio_existe.descripcion,
                                                                  'clase': examen.idclase.nombre_curso ,'imagen': examen.imagen,
                                                                   'resultado': examen.resultado, 'tiempo_realizacion': examen.tiemporealizacion, 
                                                                   'intentos': examen.intentos,'nota':examen.nota, 
                                                                   'bien_mal': examen.booleano, 'fecha': examen.fecha})

            else:
                response_data = {'result':'fail', 'message':'No se ha encontrado el usuario'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}           
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def estado_ejercicios(request):
    """
        {
        data:
            {
            "token":"token"
            "ids":[{"idalumno":"idalumno"}]
            }
        }
    
    """
    data = []
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        ids = data.get('ids', '')               
        usuario_existe = Tokenregister.objects.filter(token=token)
        if usuario_existe.count() > 0:
            response_data = {'estados': [], 'result': 'ok'}
            for id in ids:
                id_alumno = id.get('idalumno')
                for corregir in Corregir.objects.filter(idusuario=id_alumno):
                    response_data['estados'].append({'estado':  corregir.estado, 'idalumno': id_alumno})
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}           
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
