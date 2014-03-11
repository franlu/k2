#-*- coding: utf-8 -*-
import django.contrib.auth as auth
import django.http as http

from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from k2Usuario.models import Alumno, Profesor,Clase, Tokenregister
from k2Ejercicio.models import Ejercicio, Curso, Materia
from k2utils.token import id_generator

import datetime
import json
import pytz


@csrf_exempt
def cursos_ejercicios(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        Esta vista devuelve los cursos de los ejercicios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            response_data = {'result':'ok', 'cursos_ejercicios':[], 'cursos_ejercicios_favoritos':[]}
            for curso in Curso.objects.all():
                es_favorito=False
                for favorito in curso.favorito.all():
                    if favorito.id == cojer_usuario.userid.id:
                        es_favorito=True

                if es_favorito:
                    response_data['cursos_ejercicios_favoritos'].append({'idcurso': curso.id, 'nombre': curso.nombre})
                else:
                    response_data['cursos_ejercicios'].append({'idcurso': curso.id, 'nombre': curso.nombre})


        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return http.HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def materias_ejercicios(request):
    """
        {
        data:
            {
            "idcurso":"idcurso"
            "token":"token"
            }
        }
        Esta vista devuelve las materias de los ejercicios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcurso = data.get('idcurso', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            id_curso = Curso.objects.get(id=idcurso)
            response_data = {'result':'ok', 'materias_ejercicios':[], 'materias_ejercicios_favoritos':[]}
            for materias in Materia.objects.filter(curso=id_curso):
                es_favorito=False
                for favorito in materias.favorito.all():
                    if favorito.id==cojer_usuario.userid.id:
                        es_favorito=True

                if es_favorito:
                    response_data['materias_ejercicios_favoritos'].append({'idmateria': materias.id, 'nombre': materias.nombre})
                else:
                    response_data['materias_ejercicios'].append({'idmateria': materias.id, 'nombre': materias.nombre})


        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return http.HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return http.HttpResponse(json.dumps(response_data), mimetype="application/json")