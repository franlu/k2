#-*- coding: utf-8 -*-
import django.contrib.auth as auth
import django.http as http

from annoying.functions import get_object_or_None
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from k2Usuario.models import Alumno, Profesor,Clase, Tokenregister
from k2Ejercicio.models import Ejercicio, Curso, Materia, Tema, Dificultad, Notificacion
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

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

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
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def temas_ejercicios(request):
    """
        {
        data:
            {
            "idmateria":"idmateria"
            "token":"token"
            }
        }
        Esta vista devuelve las materias de los ejercicios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idmateria = data.get('idmateria', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            id_materia = Materia.objects.get(id=idmateria)
            response_data = {'result':'ok', 'temas_publicos':[], 'temas_publicos_favoritos':[], 'temas_privados':[], 'temas_privados_favoritos':[]}
            for temas in Tema.objects.filter(materia=id_materia):
                if temas.tipo == "publico":

                    es_favorito=False
                    for favorito in temas.favorito.all():
                        if favorito.id == cojer_usuario.userid.id:
                            es_favorito=True

                    if es_favorito:
                        response_data['temas_publicos_favoritos'].append({'idtema': temas.id, 'nombre': temas.nombre, 'tipo': temas.tipo})
                    else:
                        response_data['temas_publicos'].append({'idtema': temas.id, 'nombre': temas.nombre, 'tipo': temas.tipo})


                else:
                    if int(temas.tipo) == int(cojer_usuario.userid.id):
                        es_favorito=False
                        for favorito in temas.favorito.all():
                            if favorito.id == cojer_usuario.userid.id:
                                es_favorito=True


                        if es_favorito:
                            response_data['temas_privados_favoritos'].append({'idtema': temas.id, 'nombre': temas.nombre, 'tipo': temas.tipo})
                        else:
                            response_data['temas_privados'].append({'idtema': temas.id, 'nombre': temas.nombre, 'tipo': temas.tipo})

        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def dificultad_ejercicios(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        Esta vista devuelve las dificultades de los ejercicios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            response_data = {'result':'ok', 'dificultades':[]}
            for dificultad in Dificultad.objects.all():
                response_data['dificultades'].append({'iddificultad': dificultad.id, 'nombre': dificultad.nombre})

        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def ejercicios_totales(request):
    """
        {
        data:
            {
            "token":"token"
            "idcurso":"idcurso"
            "idmateria":"idmateria"
            "iddificultad":"iddificultad"
            "idtema":"idtema"
            "tipo":"tipo"
            }
        }
        Esta vista devuelve los ejercicios correspondientes a una materia y un ejercicio.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcurso = data.get('idcurso', 'null')
        idmateria = data.get('idmateria', 'null')
        iddificultad = data.get('iddificultad', 'null')
        idtema = data.get('idtema', 'null')
        tipo = data.get('tipo', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            curso_existe = Curso.objects.filter(id=idcurso)
            materia_existe = Materia.objects.filter(id=idmateria)
            if curso_existe.count() > 0 and materia_existe.count() > 0:
                curso_existe = Curso.objects.get(id=idcurso)
                materia_existe = Materia.objects.get(id=idmateria)
                dificultad_existe = Dificultad.objects.filter(id=iddificultad)
                if dificultad_existe.count() > 0:
                    dificultad_existe = Dificultad.objects.get(id=iddificultad)
                    tema_existe = Tema.objects.filter(id=idtema)
                    if tema_existe.count() > 0:
                        tema_existe = Tema.objects.get(id=idtema)
                        response_data = {'result':'ok', 'ejercicios':[]}
                        for ejercicio in Ejercicio.objects.filter(materia=materia_existe, curso=curso_existe, dificultad=dificultad_existe, tema=tema_existe):
                            response_data['ejercicios'].append({'titulo': ejercicio.titulo, 'idejercicio': ejercicio.id})
                    else:
                        response_data = {'result':'fail', 'message':'No existe el tema seleccionado'}
                else:
                    response_data = {'result':'fail', 'message':'No existe la dificultad seleccionada'}
            else:
                response_data = {'result':'fail', 'message':'No existe la materia o el curso'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

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
        Esta vista le manda al usuario los detalles del ejercicio del cual ha enviado el id para mostrar
        en la lista.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:

            comprobar_ejercicio = Ejercicio.objects.filter(id=idejercicio)
            if comprobar_ejercicio.count() > 0:
                obtener_ejercicio = Ejercicio.objects.get(id=idejercicio)
                response_data = {'result': 'ok', 'titulo': obtener_ejercicio.titulo, 'descripcion': obtener_ejercicio.descripcion, 'idejercicio': obtener_ejercicio.id,'dificultad': obtener_ejercicio.dificultad.nombre }
            else:
                response_data = {'result':'fail', 'message': 'Ejercicio no encontrado'}

        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def favorito_crear(request):
    """
        {
        data:
            {
            "tipo":"tipo"
            "idfavorito":"idfavorito"
            "token":"token"
            }
        }
        Este metodo pone como favorito un curso, una materia o un tema.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        tipo = data.get('tipo', 'null')
        idfavorito = data.get('idfavorito', 'null')

        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)

            if tipo == "curso":
                cursos_ejercicios = Curso.objects.get(id=idfavorito)
                cursos_ejercicios.favorito.add(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Curso marcado como favorito'}
            if tipo == "materia":
                materia_ejercicios = Materia.objects.get(id=idfavorito)
                materia_ejercicios.favorito.add(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Materia marcada como favorita'}
            if tipo == "tema":
                temas_ejercicios = Tema.objects.get(id=idfavorito)
                temas_ejercicios.favorito.add(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Tema marcado como favorito'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def favorito_borrar(request):
    """
        {
        data:
            {
            "tipo":"tipo"
            "idfavorito":"idfavorito"
            "token":"token"
            }
        }
        Este metodo borra como favorito un curso, una materia o un tema.
    """

    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        tipo = data.get('tipo', 'null')
        idfavorito = data.get('idfavorito', 'null')

        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)

            if tipo == "curso":
                cursos_ejercicios = Curso.objects.get(id=idfavorito)
                cursos_ejercicios.favorito.remove(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Curso quitado como favorito'}
            if tipo == "materia":
                materia_ejercicios = Materia.objects.get(id=idfavorito)
                materia_ejercicios.favorito.remove(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Materia quitado como favorita'}
            if tipo == "tema":
                temas_ejercicios = Tema.objects.get(id=idfavorito)
                temas_ejercicios.favorito.remove(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Tema quitado como favorito'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def consultar_notificacion(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
    esta vista devuelve las notificaciones tales como ejercicios pendientes, conexiones etc
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', '')
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            token_existe = Tokenregister.objects.get(token=token)
            notificaciones_total = Notificacion.objects.filter(usuario=token_existe.userid)
            response_data = {'result':'ok', 'notificaciones':[]}
            for notificacion_individual in notificaciones_total:
                response_data['notificaciones'].append({'idnotificacion': notificacion_individual.id, 'tipo':notificacion_individual.tipo, 'mensaje':notificacion_individual.mensaje})
                if notificacion_individual.fecha < datetime.datetime.now(pytz.utc):
                    notificacion_individual.delete()
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

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

        data = json.loads(request.POST['data'])
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
                guardar_notificacion = Notificacion(usuario=usuario_existe, fecha=fecha_expiracion, tipo=tipo, mensaje=mensaje)
                guardar_notificacion.save()
                response_data = {'result':'ok', 'message':'Notificacion creada'}
            else:
                response_data = {'result':'fail', 'message':'Usuario no encontrado'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

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
        data = json.loads(request.POST['data'])
        token = data.get('token', '')
        idnotificacion = data.get('idnotificacion', '')
        token_existe = Tokenregister.objects.filter(token=token)
        if token_existe.count() > 0:
            token_existe = Tokenregister.objects.get(token=token)
            notificaciones_total = Notificacion.objects.filter(usuario=token_existe.userid, id=idnotificacion)
            if notificaciones_total.count() > 0:
                notificaciones_total = Notificacion.objects.get(usuario=token_existe.userid, id=idnotificacion)
                notificaciones_total.delete()
                response_data = {'result':'ok', 'message':'Notificacion eliminada'}
            else:
                response_data = {'result':'fail', 'message':'Notificacion no encontrada'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.args}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
