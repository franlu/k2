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
from konecta2app.models import Permisos, MateriasEjercicios, Incidencias, Notificacion, CursosEjercicios, EjerciciosPendientes, EjerciciosClase, Examenes
from konecta2app.models import TiposEjercicios, Tema, Tokenregister, Cursos, Observaciones, Profesor, Alumno, Invitado, Ejercicios, Dificultad, Corregir, Controles, Globales
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
from datetime import datetime

from konecta2 import config

"""
---------------------------------Gestion de ejercicios Android by brian
"""

@csrf_exempt
def get_fecha(fecha):
    """
        
    """
    date_str = fecha
    formatter_string = "%d/%m/%Y" 
    datetime_object = datetime.strptime(date_str, formatter_string)
    date_object = datetime_object.date()
    return date_object


@csrf_exempt
def get_elementos(request):
    """
        {
        data:
            {
            "token":"token"
            "elemento":"elemento"
            }
        }
        
        sirve para dar todos los elementos de una tabla dependiendo de que se quiera
        elemento puede ser :
            materias
        
    """
    
    try:
        data = simplejson.loads(request.POST['data'])
        elemento=data.get('elemento','materias')
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            
            
            if elemento == "materias":
                response_data = {'result':'ok', 'materias':[]} 
                for materia in MateriasEjercicios.objects.all():
                    response_data['materias'].append({'id': materia.idmateria, 'nombre': materia.nombre, 'idcurso':materia.curso.idcursos}) 
            
            if elemento == "cursos":
                response_data = {'result':'ok', 'cursos':[]}
                for curso in Cursos.objects.all():
                    response_data['cursos'].append({'id':curso.idcurso,'nombre':curso.nombre_curso})
            
            if elemento == "alumnos":
                response_data = {'result':'ok', 'alumnos':[]} 
                for alumno in Alumno.objects.all():
                    response_data['alumnos'].append({'id': alumno.idusuario.id, 'nombre': alumno.nombre, 'apellido1':alumno.apellido1, 'apellido2':alumno.apellido2}) 
            
            if elemento == "tipos":
                response_data = {'result':'ok', 'tipos':[]} 
                for tipo in TiposEjercicios.objects.all():
                    response_data['tipos'].append({'id': tipo.idtipo, 'nombre': tipo.nombre}) 
             
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


@csrf_exempt
def busqueda_filtros(request):
    """
        {
        data:
            {
            "token":"token"
            "idalumno"
            "idmateria":"idmateria"
            "idtema"
            "idclase"
            "idtipo"
            "fechainicio"
            "fechafin"
            
            }
        }
        
    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')
        idalumno = data.get('idalumno', 'null')
        idmateria = data.get('idmateria', 'null')
        idtema=data.get('idtema','null')
        idclase=data.get('idclase','null')
        idtipo=data.get('idtipo','null')
        fechainicio=data.get('fechainicio','null')
        fechafin=data.get('fechafin','null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            response_data = {'result':'ok','ejercicios':[],'mensaje':[]}
            if idtipo == 'null':#tipo es null
                response_data['mensaje'].append('tipo null')
                if idalumno!='null':#si me envia un alumno filtramos lo de ese alumno
                    #si el tema es null
                    if idtema!='null':
                        #si la materia no es null
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                       #materia no es null                 
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                       #materia no es null     
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        #materia no es null    
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        #y si materia si es null                
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                  
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                            
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    #y si el tema si es null                
                    else:
                        response_data['mensaje'].append('tema null')
                        #si la materia no es null
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
              
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                            
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        #si la materia si es null                
                        else:
                            response_data['mensaje'].append("materia null")
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
              
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                            
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                else:#si no ponemos todos los examens y ejercicios
                    response_data['mensaje'].append('alumno null')
                    #si el tema no es null
                    if idtema!='null':
                        #si lamateria no es null
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                  
                            for ejercicio in Controles.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                            
                            for ejercicio in EjerciciosClase.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                            for ejercicio in Globales.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        #si la materia es null
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Examenes.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                  
                            for ejercicio in Controles.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                            
                            for ejercicio in EjerciciosClase.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                            for ejercicio in Globales.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})                
                    #en el caso de que sea null el tema
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                                        
                            for ejercicio in Controles.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                            
                            for ejercicio in EjerciciosClase.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                            for ejercicio in Globales.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                           'fecha':ejercicio.fecha})
                        #materia si es null
                        else:
                            response_data['mensaje'].append('materia es null')
                            for ejercicio in Examenes.objects.all():
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                                        
                            for ejercicio in Controles.objects.all():
                                       response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                            
                            for ejercicio in EjerciciosClase.objects.all():
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                            
                            for ejercicio in Globales.objects.all():
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                               
            if idtipo == 1:#tipo examenes
                if idalumno!='null':
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Examenes.objects.filter(idusuario=idalumno):
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                else:
                    response_data['mensaje'].append('alumno null')
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Examenes.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in Examenes.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Examenes.objects.all():
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    
            if idtipo == 2:#tipo controles
                if idalumno!='null':
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Controles.objects.filter(idusuario=idalumno):
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                else:
                    response_data['mensaje'].append('alumno null')
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in Controles.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Controles.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in Controles.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Controles.objects.all():
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})           
                          
            if idtipo == 3:#tipo ejerciciosClase
                if idalumno!='null':
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    else:
                        if idmateria!='null':
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in EjerciciosClase.objects.filter(idusuario=idalumno):
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                else:
                    response_data['mensaje'].append('alumno null')
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in EjerciciosClase.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in EjerciciosClase.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in EjerciciosClase.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in EjerciciosClase.objects.all():
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        
                                
            if idtipo == 4:#tipo globales
                if idalumno!='null':
                    # si el tema es distinto de 'null'
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    #si no mandamos todos los ejercicios de todos los temas                
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Globales.objects.filter(idusuario=idalumno):
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                else:
                    response_data['mensaje'].append('alumno null')
                    # si el tema es distinto de null
                    if idtema!='null':
                        if idmateria!='null':
                            for ejercicio in Globales.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Globales.objects.all():
                                    if ejercicio.idejercicio.tema.idtema==idtema:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                    #si no mandamos todos los ejercicios de todos los temas                
                    else:
                        response_data['mensaje'].append('tema null')
                        if idmateria!='null':
                            for ejercicio in Globales.objects.all():
                                if ejercicio.idejercicio.materia.idmateria==idmateria:
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        else:
                            response_data['mensaje'].append('materia null')
                            for ejercicio in Globales.objects.all():
                                        response_data['ejercicios'].append({'titulo':ejercicio.idejercicio.titulo,
                                                                            'descripcion':ejercicio.idejercicio.descripcion,
                                                                            'idejercicio':ejercicio.idejercicio.idejercicio,
                                                                            'dificultad':ejercicio.idejercicio.dificultad.iddificultad,
                                                                            'interfaz':ejercicio.idejercicio.interfaz,
                                                                            'imagen':ejercicio.idejercicio.imagen,
                                                                            'urlimagen':ejercicio.imagen,
                                                                            'nota':ejercicio.nota,
                                                                            'fecha':ejercicio.fecha})
                        
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
   