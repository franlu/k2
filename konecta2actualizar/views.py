#-*- encoding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from konecta2app.models import Permisos, MateriasEjercicios, Incidencias, Notificacion, CursosEjercicios
from konecta2app.models import Tema, Tokenregister, Cursos, Observaciones, Profesor, Alumno, Invitado, Ejercicios, Dificultad, Corregir
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from base64 import b64decode

@csrf_exempt
def actualizar_k2(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        Esta vista actualiza el servidor central.
    """
    try:
        data = simplejson.loads(request.POST['data'])
        token = data.get('token', 'null')      
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_usuario = Tokenregister.objects.get(token=token)
            usuario = User.objects.get(id=comprobar_usuario.userid.id)
            if usuario.is_staff:
                response_data = {'ejercicios_array':[], 'cursos_array':[], 'materias_array':[], 'temas_array':[]}
                for ejercicios in Ejercicios.objects.filter(estado=""):
                    if ejercicios.imagen != "null":
                        file = open(ejercicios.imagen, "r")
                        photo_bin = file.read()
                        file.close()
                        photo_b64 = base64.b64encode(photo_bin)
                    ejercicios.estado = "enviado"
                    response_data['ejercicios_array'].append({'idcentro':ejercicios.idcentro, 'idejercicio': ejercicios.idejercicio, 'titulo': ejercicios.titulo, 'imagen':photo_b64, 'descripcion':ejercicios.descripcion, 
                                                              'materia':ejercicios.materia.idmateria, 'curso':ejercicios.curso.idcursos, 'dificultad': ejercicios.dificultad.iddificultad, 'tema': ejercicios.tema.idtema,
                                                              'resultado': ejercicios.resultado, 'calculadora': ejercicios.calculadora, 'interfaz': ejercicios.interfaz, 'consejo': ejercicios.consejo})
                    ejercicios.save()
                for curso in CursosEjercicios.objects.all():
                    response_data['cursos_array'].append({'nombre':curso.nombre, 'idcurso': curso.idcursos})
                for materias in MateriasEjercicios.objects.all():
                    response_data['materias_array'].append({'nombre': materias.nombre, 'idmateria': materias.idmateria})
                for temas  in Tema.objects.all():
                    response_data['temas_array'].append({'nombre': temas.nombre, 'idtema': temas.idtema, 'tipo': temas.tipo})
            else:
                response_data = {'result': 'fail', 'message':'No eres staff'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")