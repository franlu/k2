#-*- coding: utf-8 -*-
import django.contrib.auth as auth
import django.http as http

from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from k2Usuario.models import Alumno, Profesor,Clase, Tokenregister
from k2Ejercicio.models import Ejercicio, Curso, Materia, Tema, Dificultad, Notificacion, EjercicioEnviado,EstadoEjercicios
from k2utils import tags

import datetime
import json
import pytz



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
            alumno=Alumno.objects.get(idusuario=token_usuario.userid)
            comprobar_ejercicios= EjercicioEnviado.objects.filter(alumno=alumno)
            if comprobar_ejercicios.count() > 0:
                response_data = {'result': 'ok', 'ejercicios': []}
                for ejercicios in comprobar_ejercicios:
                    obtener_ejercicio = Ejercicio.objects.filter(id=ejercicios.id)
                    if obtener_ejercicio.count() > 0:
                        obtener_ejercicio = Ejercicio.objects.get(id=ejercicios.id)
                        response_data['ejercicios'].append({'fecha': str(ejercicios.fecha_envio),
                                                            'idcorregir':ejercicios.id,
                                                            'idprofesor': ejercicios.profesor.idusuario.id,
                                                            'titulo': obtener_ejercicio.titulo,
                                                            'descripcion': obtener_ejercicio.descripcion,
                                                            'dificultad': obtener_ejercicio.dificultad.nombre,
                                                            'idejercicio': obtener_ejercicio.id,
                                                            'tipo': obtener_ejercicio.tipo.id,
                                                            'materia': obtener_ejercicio.materia.nombre,
                                                            'idmateria': obtener_ejercicio.materia.id})
            else:
                response_data = {'result':'fail', 'message':'Ejercicio no encontrado'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")