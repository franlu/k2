#-*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.template import RequestContext

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

from konecta2 import config

@csrf_exempt
def alumnos(request):
    """
		{
		data:
			{
			"token":"token"
			"idcurso":"idcurso"
			}
		}
    Esta vista es para que el profesor pueda ver todos los alumnos tanto conectados como desconectados, como
    invitados.
    """
    data = []
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcurso = data.get('idcurso', 'null')
        usuario_existe = Tokenregister.objects.filter(token=token)

        if usuario_existe.count() > 0:
            response_data = {'result': 'ok', 'alumnos_registrados':[]}
            clase_buscada = Cursos.objects.get(idcurso=idcurso)
            alumnos_clase = Alumno.objects.filter(curso=clase_buscada)
            invitados_clase = Invitado.objects.filter(curso=clase_buscada)            

            if invitados_clase.count() > 0:
                for invitados_unidad in invitados_clase:
                    response_data['alumnos_registrados'].append({'clase':clase_buscada.nombre_curso, 'nombre': invitados_unidad.nombre, 'estado': 'Invitado', 'id': invitados_unidad.idusuario.id})                
            if alumnos_clase.count() > 0:
                for alumnos_unidad in alumnos_clase:
                    response_data['alumnos_registrados'].append({'clase':clase_buscada.nombre_curso, 'nombre': alumnos_unidad.nombre, 'estado': alumnos_unidad.estado, 'id': alumnos_unidad.idusuario.id})

        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
       	
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def clases_profesor(request):
    """
		{
		data:
			{
			"token":"token"
			}
		}
    Esta vista le mostrará al profesor sus clases cuando se logea.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            cojer_usuario = Profesor.objects.get(idusuario=token_usuario.userid.id)
            response_data = {'result': 'ok', 'cursos': []}
            for clases in cojer_usuario.curso.all():
                response_data['cursos'].append({'idcurso': clases.idcurso, 'nombre': clases.nombre_curso })
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}       	
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def registrar_ejercicio(request):
    """
		{
		data:
			{
            "idcentro":"idcentro"
            "idtema":"idtema"
            "interfaz":"interfaz"
			"descripcion":"descripcion"
			"resultado":"resultado"
			"titulo":"titulo"
			"imagen":"imagen"
			"dificultad":"dificultad"
			"token":"token"
			"idmateria":"idmateria"
			"idcurso":"idcurso"
			"calculadora":"calculadora"
            "resultado":"resultado"
            "extension":"extension"
            "consejo":"consejo"
			}
		}
        Esta vista es para registrar un ejercicio. A esta se le envia la imagen en base64 y ya se
        decodifica y se guarda en la carpeta correspondiente. En la base de datos se guarda la url.
    """

    try:
        data = json.loads(request.POST['data'])
        
        token = data.get('token', 'null')
        idcentro = data.get('idcentro', 'null')
        idtema = data.get('idtema', 'null')
        interfaz = data.get('interfaz', 'null')
        descripcion = data.get('descripcion', 'null')
        resultado = data.get('resultado', 'null')
        titulo = data.get('titulo', 'null')
        dificultad = data.get('dificultad', 'null')
        imagen = data.get('imagen', 'null')
        materia = data.get('idmateria', 'null')
        curso = data.get('idcurso', 'null')
        extension = data.get('extension', 'null')
        calculadora = data.get('calculadora', 'null')
        consejo = data.get('consejo', 'null')
        tipo = data.get('tipo', '')        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        import pdb
        pdb.set_trace()
        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            comprobar_profesor = Profesor.objects.filter(idusuario=token_usuario.userid.id)
            if comprobar_profesor.count() > 0:
                profesor = Profesor.objects.get(idusuario=token_usuario.userid.id)
                materia_recuperada = MateriasEjercicios.objects.get(idmateria=materia)
                curso_recuperado = CursosEjercicios.objects.get(idcursos=curso)

                if imagen != "null":
                    datetime_now = str(datetime.datetime.now())
                    ruta_imagen = config.ruta_imagen_1 + datetime_now + "." + extension
                    ruta_imagen = ruta_imagen.replace(" ", "+")
                    ruta_imagen2 = config.ruta_imagen_konecta2 + ruta_imagen
                    ruta_imagen2 = ruta_imagen2.replace(" ","+")
                    file = open(ruta_imagen2, "w")
                    image_b64 = imagen.replace(" ","+")
                    image_bin = base64.b64decode(image_b64)
                    file.write(image_bin)
                    file.close()
                    imagen_o_default = "Ejercicio guardado con imagen propia"
                else:
                    ruta_imagen = config.ruta_imagen_default
                    imagen_o_default = "Ejercicio guardado con imagen default"

                dificultad_ejercicio = Dificultad.objects.get(iddificultad= dificultad)
                tema_ejercicio = Tema.objects.get(idtema=idtema)


                ejercicio_guardado = Ejercicios(tipo=tipo,
                titulo=titulo, idcentro=idcentro, tema=tema_ejercicio, 
                interfaz=interfaz, idprofesor=profesor,
                descripcion=descripcion, dificultad=dificultad_ejercicio, 
                imagen=ruta_imagen, materia=materia_recuperada, curso=curso_recuperado,
                calculadora=calculadora, resultado=resultado, consejo=consejo)

                ejercicio_guardado.save()
                response_data = {'result': 'ok', 'message': imagen_o_default}
            else:
                response_data = {'result': 'fail', 'message': 'El usuario no es un profesor'}            	
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except Exception as e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def modificar_ejercicio(request):
    """
        {
        data:
            {
            "idejercicio":"idejercicio"
            "descripcion":"descripcion"
            "resultado":"resultado"
            "titulo":"titulo"
            "imagen":"imagen"
            "dificultad":"dificultad"
            "token":"token"
            "materia":"materia"
            "curso":"curso"
            "tema":"tema"
            "calculadora":"calculadora"
            "consejo":"consejo"
            "interfaz":"interfaz"
            }
        }
        Esta vista es para modificar un ejercicio. A esta se le envia la imagen en base64 y ya se
        decodifica y se guarda en la carpeta correspondiente. En la base de datos se guarda la url.
    """
    try:
        data = json.loads(request.POST['data'])
        idejercicio = data.get('idejercicio')
        token = data.get('token', 'null')
        descripcion = data.get('descripcion', 'null')
        resultado = data.get('resultado', 'null')
        titulo = data.get('titulo', 'null')
        dificultad = data.get('dificultad', 'null')
        imagen = data.get('imagen', 'null')
        materia = data.get('idmateria', 'null')
        curso = data.get('idcurso', 'null')
        tema = data.get('idtema', 'null')
        calculadora = data.get('calculadora', 'null')
        consejo = data.get('consejo', 'null')
        interfaz = data.get('interfaz', 'null')
        tipo = data.get('tipo', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            comprobar_profesor = Profesor.objects.filter(idusuario=token_usuario.userid.id)
            if comprobar_profesor.count() > 0:
                ejercicio_buscado = Ejercicios.objects.filter(idejercicio=idejercicio)
                if ejercicio_buscado.count() > 0:
                    ejercicio_buscado = Ejercicios.objects.get(idejercicio=idejercicio)

                    id_materia = MateriasEjercicios.objects.get(idmateria=materia)
                    id_curso = CursosEjercicios.objects.get(idcursos=curso)
                    id_tema = Tema.objects.get(idtema=tema)
                    if imagen != "null":
                        datetime_now = str(datetime.datetime.now())
                        ruta_imagen = ejercicio_buscado.imagen
                        file = open(config.ruta_imagen_konecta2 + ruta_imagen, "w")
                        image_b64 = imagen.replace(" ","+")
                        image_bin = base64.b64decode(image_b64)
                        file.write(image_bin)
                        file.close()
                    dificultad_ejercicio = Dificultad.objects.get(iddificultad=dificultad)
                    ejercicio_buscado.titulo = titulo
                    ejercicio_buscado.descripcion = descripcion
                    ejercicio_buscado.resultado = resultado
                    ejercicio_buscado.dificultad = dificultad_ejercicio 
                    ejercicio_buscado.materia = id_materia
                    ejercicio_buscado.curso = id_curso 
                    ejercicio_buscado.calculadora = calculadora
                    ejercicio_buscado.tema = id_tema
                    ejercicio_buscado.idprofesor = token_usuario.userid
                    ejercicio_buscado.consejo = consejo
                    ejercicio_buscado.interfaz = interfaz
                    ejercicio_buscado.tipo = tipo
                    ejercicio_buscado.save()
                    response_data = {'result': 'ok'}
                else:
                    response_data = {'result':'fail', 'message':'Ejercicio no encontrado'}
            else:
                response_data = {'result': 'fail', 'message': 'El usuario no es un profesor'}               
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def enviar_ejercicio_individual(request):
    """
        {
        data:
            {
            "token":"token"
            "idejercicio":"idejercicio"
            "idalumno":"idalumno" //la de user    
            }
        }
        Esta vista le envia un ejercicio a un alumno.
    """
    import pdb
    pdb.set_trace()

    try:
        print "hola"
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        idalumno = data.get('idalumno', 'null')
        todos=Tokenregister.objects.all()
        print todos
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        print comprobar_usuario
        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            print token
            comprobar_profesor = Profesor.objects.filter(idusuario=token_usuario.userid.id)
            if comprobar_profesor.count() > 0:
                obtener_profesor = Profesor.objects.get(idusuario=token_usuario.userid.id)
                obtener_usuario = User.objects.filter(id=idalumno)
                if obtener_usuario.count() > 0:
                    obtener_usuario = User.objects.get(id=idalumno)
                    obtener_ejercicio = Ejercicios.objects.filter(idejercicio=idejercicio)
                    if obtener_ejercicio.count() > 0:
                        fecha = datetime.datetime.now(pytz.utc)+datetime.timedelta(0,7200)
                        fecha = str(fecha)
                        obtener_ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                        corregir_ejercicio = Corregir(idusuario=obtener_usuario, estado="sin hacer",urlimagen="null", materia=obtener_ejercicio.materia, idejercicio=obtener_ejercicio)
                        corregir_ejercicio.save()
                        ejercicio_pendiente = EjerciciosPendientes(idprofesor=obtener_profesor, idcorregir=corregir_ejercicio,idejercicio=obtener_ejercicio, idalumno=obtener_usuario, fecha=fecha)
                        ejercicio_pendiente.save()
                        print "llego"
                        response_data = {'result': 'ok', 'message': 'Ejercicio enviado'}
                    else:
                        response_data = {'result': 'fail', 'message': 'Ejercicio no encontrado'}                
                else:
                    response_data = {'result': 'fail', 'message': 'Usuario no encontrado'}
            else:
                response_data = {'result': 'fail', 'message': 'El usuario no es un profesor'}               
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        print "mensjae :", e.message
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def enviar_ejercicio_todos(request):
    """
        {
        data:
            {
            "token":"token"
            "idejercicio":"idejercicio"
            "idalumnos":[{
                        "idalumno":"idalumno"
                        }]
            }
        }
        Esta vista con el id del ejercicio, se lo manda a todos los alumnos que se envien.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        idalumnos = data.get('idalumnos', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            comprobar_profesor = Profesor.objects.filter(idusuario=token_usuario.userid.id)
            if comprobar_profesor.count() > 0:
                obtener_profesor = Profesor.objects.get(idusuario=token_usuario.userid.id)
                obtener_ejercicio = Ejercicios.objects.filter(idejercicio=idejercicio)
                if obtener_ejercicio.count() > 0:
                    obtener_ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                    fecha = datetime.datetime.now(pytz.utc)+datetime.timedelta(0,7200)
                    fecha = str(fecha)
                    for alumno in idalumnos:
                        id_alumno = alumno.get('idalumno')
                        obtener_usuario = User.objects.filter(id=id_alumno)
                        if obtener_usuario.count() > 0:
                            obtener_usuario = User.objects.get(id=id_alumno)
                            corregir_ejercicio = Corregir(idusuario=obtener_usuario, urlimagen="null", estado="sin hacer", materia=obtener_ejercicio.materia, idejercicio=obtener_ejercicio)
                            corregir_ejercicio.save()
                            ejercicio_pendiente = EjerciciosPendientes(idejercicio=obtener_ejercicio, idcorregir=corregir_ejercicio,idprofesor=obtener_profesor, idalumno=obtener_usuario, fecha=fecha)
                            ejercicio_pendiente.save()
                            
                    response_data = {'result': 'ok', 'message': 'Operacion realizada'}
                else:
                    response_data = {'result': 'fail', 'message': 'Ejercicio no encontrado'}                     
            else:
                response_data = {'result': 'fail', 'message': 'El usuario no es un profesor'}               
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def informacion_usuario(request):
    """
        {
        data:
            {
            "token":"token"
            "tipo":"tipo"
            "idusuario":"idusuario"
            }
        }
        Esta vista devuelve los datos de un alumno.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        tipo = data.get('tipo', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            if tipo == "Profesores":
                usuario_existe = User.objects.filter(id=idusuario)
                if usuario_existe.count() >0:
                    usuario_existe = User.objects.get(id=idusuario)
                    profesor_existe = Profesor.objects.filter(idusuario=usuario_existe)
                    if profesor_existe.count() > 0:
                        profesor_existe = Profesor.objects.get(idusuario=usuario_existe)
                        permisos_profesor = Permisos.objects.get(idusuario=usuario_existe)
                        response_data = {'result':'ok', 
                        'nombre':profesor_existe.nombre,
                        'username':usuario_existe.username,
                        'last_login':str(usuario_existe.last_login+datetime.timedelta(0, 7200)),
                        'primer_apellido': profesor_existe.apellido1, 
                        'segundo_apellido': profesor_existe.apellido2,
                        'idusuario': profesor_existe.idusuario.id,
                        'estado': profesor_existe.estado,
                        'crear_usuario': permisos_profesor.crear_usuario,
                        'ver_todos_usuarios': permisos_profesor.ver_todos_usuarios,
                        'modificar_usuario': permisos_profesor.modificar_usuario,
                        'eliminar_usuario': permisos_profesor.eliminar_usuario,
                        'ver_notas': permisos_profesor.ver_notas,
                        'modificar_notas': permisos_profesor.modificar_notas,
                        'eliminar_ejercicios': permisos_profesor.eliminar_ejercicio,
                        'crear_ejercicios': permisos_profesor.crear_ejercicio,
                        'modificar_ejercicios': permisos_profesor.modificar_ejercicio,
                        'curso': []
                        }
                        for cursos in profesor_existe.curso.all():
                            response_data['curso'].append({'idcurso': cursos.idcurso, 'nombre_curso': cursos.nombre_curso})
                    else:
                        response_data = {'result':'fail', 'message': 'El perfil del profesor no existe'}
                else:
                    response_data =  {'result':'fail', 'message': 'El usuario no existe'}
            if tipo == "Alumnos":    
                usuario_existe = User.objects.filter(id=idusuario)
                if usuario_existe.count() >0:
                    usuario_existe = User.objects.get(id=idusuario)
                    alumno_existe = Alumno.objects.filter(idusuario=usuario_existe)
                    if alumno_existe.count() > 0:
                        alumno_existe = Alumno.objects.get(idusuario=usuario_existe)
                        response_data = {'result':'ok', 
                        'nombre':alumno_existe.nombre,
                        'username':usuario_existe.username,
                        'last_login':str(usuario_existe.last_login+datetime.timedelta(0, 7200)), 
                        'primer_apellido': alumno_existe.apellido1, 
                        'segundo_apellido': alumno_existe.apellido2,
                        'idusuario': alumno_existe.idusuario.id,
                        'estado': alumno_existe.estado,
                        'curso': []
                        }
                        for cursos in alumno_existe.curso.all():
                            response_data['curso'].append({'idcurso': cursos.idcurso, 'nombre_curso': cursos.nombre_curso})
                    else:
                        response_data = {'result':'fail', 'message': 'El perfil del alumno no existe'}
                else:
                    response_data =  {'result':'fail', 'message': 'El usuario no existe'}

            if tipo == "Invitados":
                usuario_existe = User.objects.filter(id=idusuario)
                if usuario_existe.count() >0:
                    usuario_existe = User.objects.get(id=idusuario)
                    invitado_existe = Invitado.objects.filter(idusuario=usuario_existe)
                    if invitado_existe.count() > 0:
                        invitado_existe = Invitado.objects.get(idusuario=usuario_existe)
                        response_data = {'result':'ok', 
                        'nombre':invitado_existe.nombre,
                        'username':usuario_existe.username,
                        'last_login':str(usuario_existe.last_login+datetime.timedelta(0, 7200)), 
                        'idusuario': invitado_existe.idusuario.id,
                        'estado': invitado_existe.estado,
                        'curso': []
                        }
                        for cursos in invitado_existe.curso.all():
                            response_data['curso'].append({'idcurso': cursos.idcurso, 'nombre_curso': cursos.nombre_curso})
                    else:
                        response_data = {'result':'fail', 'message': 'El perfil del invitado no existe'}
                else:
                    response_data =  {'result':'fail', 'message': 'El usuario no existe'}


        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

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
            id_materia = MateriasEjercicios.objects.get(idmateria=idmateria)
            response_data = {'result':'ok', 'temas_publicos':[], 'temas_publicos_favoritos':[], 'temas_privados':[], 'temas_privados_favoritos':[]}
            for temas in Tema.objects.filter(materia=id_materia):
                if temas.tipo == "publico":
                    if str(temas.favorito.all()) == "[]":
                        response_data['temas_publicos'].append({'idtema': temas.idtema, 'nombre': temas.nombre, 'tipo': temas.tipo})
                    for favorito in temas.favorito.all():
                        if favorito.id == cojer_usuario.userid.id:
                            response_data['temas_publicos_favoritos'].append({'idtema': temas.idtema, 'nombre': temas.nombre, 'tipo': temas.tipo})
                        else:
                            response_data['temas_publicos'].append({'idtema': temas.idtema, 'nombre': temas.nombre, 'tipo': temas.tipo})
                else:
                    if int(temas.tipo) == int(cojer_usuario.userid.id):
                        if str(temas.favorito.all()) == "[]":
                            response_data['temas_privados'].append({'idtema': temas.idtema, 'nombre': temas.nombre, 'tipo': temas.tipo})

                        for favorito in temas.favorito.all():
                            if favorito.id == cojer_usuario.userid.id:
                                response_data['temas_privados_favoritos'].append({'idtema': temas.idtema, 'nombre': temas.nombre, 'tipo': temas.tipo})
                            else:
                                response_data['temas_privados'].append({'idtema': temas.idtema, 'nombre': temas.nombre, 'tipo': temas.tipo})

        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

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
            id_curso = CursosEjercicios.objects.get(idcursos=idcurso)
            response_data = {'result':'ok', 'materias_ejercicios':[], 'materias_ejercicios_favoritos':[]}
            for materias in MateriasEjercicios.objects.filter(curso=id_curso):
                if str(materias.favorito.all()) == "[]":
                    response_data['materias_ejercicios'].append({'idmateria': materias.idmateria, 'nombre': materias.nombre})
                for favorito in materias.favorito.all():
                    if favorito.id == cojer_usuario.userid.id:
                        response_data['materias_ejercicios_favoritos'].append({'idmateria': materias.idmateria, 'nombre': materias.nombre})
                    else:
                        response_data['materias_ejercicios'].append({'idmateria': materias.idmateria, 'nombre': materias.nombre})


        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

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
            for curso in CursosEjercicios.objects.all():
                if str(curso.favorito.all()) == "[]":
                    response_data['cursos_ejercicios'].append({'idcurso': curso.idcursos, 'nombre': curso.nombre})
                for favorito in curso.favorito.all():
                    if favorito.id == cojer_usuario.userid.id:
                        response_data['cursos_ejercicios_favoritos'].append({'idcurso': curso.idcursos, 'nombre': curso.nombre})
                    else:
                        response_data['cursos_ejercicios'].append({'idcurso': curso.idcursos, 'nombre': curso.nombre})

                    
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def crear_curso(request):
    """
        {
        data:
            {
            "nombre":"nombre"
            "token":"token"
            }
        }
        Esta vista devuelve los cursos de los ejercicios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        nombre = data.get('nombre', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            curso = CursosEjercicios(nombre=nombre)
            curso.save()
            response_data = {'result': 'ok', 'message': 'Curso guardado'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def crear_materia(request):
    """
        {
        data:
            {
            "idcurso":"idcurso"
            "nombre":"nombre"
            "token":"token"
            }
        }
        Esta vista devuelve los cursos de los ejercicios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcurso = data.get('idcurso', 'null')
        nombre = data.get('nombre', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            id_curso = CursosEjercicios.objects.get(idcursos=idcurso)
            materia = MateriasEjercicios(nombre=nombre, curso=id_curso)
            materia.save()
            response_data = {'result': 'ok', 'message': 'Materia guardada'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def crear_tema(request):
    """
        {
        data:
            {
            "idmateria":"idmateria"
            "tipo":"tipo"
            "nombre":"nombre"
            "token":"token"
            }
        }
        Esta vista devuelve los cursos de los ejercicios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        tipo = data.get('tipo', 'null')
        idmateria = data.get('idmateria', 'null')
        nombre = data.get('nombre', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            id_materia = MateriasEjercicios.objects.get(idmateria=idmateria)
            if tipo == "publico":
                tema = Tema(nombre=nombre, materia=id_materia, tipo="publico")
                tema.save()
                response_data = {'result': 'ok', 'message': 'Tema guardado tipo publico'}
            if tipo == "privado":
                cojer_usuario = Tokenregister.objects.get(token=token)
                tema = Tema(nombre=nombre, materia=id_materia, tipo=cojer_usuario.userid.id)
                tema.save()
                response_data = {'result': 'ok', 'message': 'Tema guardado tipo privado'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

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
            curso_existe = CursosEjercicios.objects.filter(idcursos=idcurso)
            materia_existe = MateriasEjercicios.objects.filter(idmateria=idmateria)
            if curso_existe.count() > 0 and materia_existe.count() > 0:
                curso_existe = CursosEjercicios.objects.get(idcursos=idcurso)
                materia_existe = MateriasEjercicios.objects.get(idmateria=idmateria)
                dificultad_existe = Dificultad.objects.filter(iddificultad=iddificultad)
                if dificultad_existe.count() > 0:                    
                    dificultad_existe = Dificultad.objects.get(iddificultad=iddificultad)
                    tema_existe = Tema.objects.filter(idtema=idtema)
                    if tema_existe.count() > 0:                    
                        tema_existe = Tema.objects.get(idtema=idtema)
                        response_data = {'result':'ok', 'ejercicios':[]}
                        for ejercicio in Ejercicios.objects.filter(materia=materia_existe, tipo=tipo, curso=curso_existe, dificultad=dificultad_existe, tema=tema_existe):
                            response_data['ejercicios'].append({'titulo': ejercicio.titulo, 'idejercicio': ejercicio.idejercicio})
                    else:
                        response_data = {'result':'fail', 'message':'No existe el tema seleccionado'}
                else:
                    response_data = {'result':'fail', 'message':'No existe la dificultad seleccionada'}
            else:
                response_data = {'result':'fail', 'message':'No existe la materia o el curso'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def ejercicios_totales_android(request):
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
            curso_existe = CursosEjercicios.objects.filter(idcursos=idcurso)
            materia_existe = MateriasEjercicios.objects.filter(idmateria=idmateria)
            if curso_existe.count() > 0 and materia_existe.count() > 0:
                curso_existe = CursosEjercicios.objects.get(idcursos=idcurso)
                materia_existe = MateriasEjercicios.objects.get(idmateria=idmateria)
                dificultad_existe = Dificultad.objects.filter(iddificultad=iddificultad)
                if dificultad_existe.count() > 0:                    
                    dificultad_existe = Dificultad.objects.get(iddificultad=iddificultad)
                    tema_existe = Tema.objects.filter(idtema=idtema)
                    if tema_existe.count() > 0:                    
                        tema_existe = Tema.objects.get(idtema=idtema)
                        response_data = {'result':'ok', 'ejercicios':[]}
                        for ejercicio in Ejercicios.objects.filter(materia=materia_existe, curso=curso_existe, dificultad=dificultad_existe, tema=tema_existe):
                            response_data['ejercicios'].append({'titulo': ejercicio.titulo, 'idejercicio': ejercicio.idejercicio})
                    else:
                        response_data = {'result':'fail', 'message':'No existe el tema seleccionado'}
                else:
                    response_data = {'result':'fail', 'message':'No existe la dificultad seleccionada'}
            else:
                response_data = {'result':'fail', 'message':'No existe la materia o el curso'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
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
                response_data['dificultades'].append({'iddificultad': dificultad.iddificultad, 'nombre': dificultad.nombre})

        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

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
                cursos_ejercicios = CursosEjercicios.objects.get(idcursos=idfavorito)
                cursos_ejercicios.favorito.add(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Curso marcado como favorito'}
            if tipo == "materia":
                materia_ejercicios = MateriasEjercicios.objects.get(idmateria=idfavorito)
                materia_ejercicios.favorito.add(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Materia marcada como favorita'}
            if tipo == "tema":
                temas_ejercicios = Tema.objects.get(idtema=idfavorito)
                temas_ejercicios.favorito.add(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Tema marcado como favorito'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

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
                cursos_ejercicios = CursosEjercicios.objects.get(idcursos=idfavorito)
                cursos_ejercicios.favorito.remove(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Curso quitado como favorito'}
            if tipo == "materia":
                materia_ejercicios = MateriasEjercicios.objects.get(idmateria=idfavorito)
                materia_ejercicios.favorito.remove(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Materia quitado como favorita'}
            if tipo == "tema":
                temas_ejercicios = Tema.objects.get(idtema=idfavorito)
                temas_ejercicios.favorito.remove(cojer_usuario.userid.id)
                response_data = {'result': 'ok', 'message': 'Tema quitado como favorito'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


@csrf_exempt
def detalles_ejercicio_java(request):
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
            comprobar_ejercicio = Ejercicios.objects.filter(idejercicio=idejercicio)
            if comprobar_ejercicio.count() > 0:
                obtener_ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                obtener_profesor = Profesor.objects.filter(idusuario=obtener_ejercicio.idprofesor.id)
                if obtener_profesor.count()>0:
                    obtener_profesor = Profesor.objects.get(idusuario=obtener_ejercicio.idprofesor.id)
                    usuario_ejercicio = obtener_profesor.nombre + obtener_profesor.apellido1
                else:
                    usuario_ejercicio = "null"
                response_data = {'result': 'ok', 'titulo': obtener_ejercicio.titulo, 'profesor':usuario_ejercicio,
                'idcurso': obtener_ejercicio.curso.idcursos, 'nombre_curso':obtener_ejercicio.curso.nombre,
                'idtema': obtener_ejercicio.tema.idtema ,'nombre_tema': obtener_ejercicio.tema.nombre,
                'descripcion': obtener_ejercicio.descripcion, 'idejercicio': obtener_ejercicio.idejercicio, 
                'imagen': obtener_ejercicio.imagen,'calculadora': obtener_ejercicio.calculadora, 
                'dificultad': obtener_ejercicio.dificultad.nombre,'interfaz':  obtener_ejercicio.interfaz,
                'idmateria': obtener_ejercicio.materia.idmateria, 'tipo':obtener_ejercicio.tipo, 'nombre_materia': obtener_ejercicio.materia.nombre, 
                'iddificultad': obtener_ejercicio.dificultad.iddificultad, 'nombre_dificultad': obtener_ejercicio.dificultad.nombre,
                'resultado': obtener_ejercicio.resultado}

            else:
                response_data = {'result':'fail', 'message': 'Ejercicio no encontrado'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def eliminar_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idejercicio":"idejercicio"
            }
        }
        Esta vista elimina el ejercicio del cual se ha mandado el id.
    """
    try:

        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            tiene_permiso = Permisos.objects.filter(idusuario=token_usuario.userid)
            if tiene_permiso.count()>0:
                tiene_permiso = Permisos.objects.get(idusuario=token_usuario.userid)
                if tiene_permiso.eliminar_ejercicio == "true":
                    comprobar_ejercicio = Ejercicios.objects.filter(idejercicio=idejercicio)
                    if comprobar_ejercicio.count() > 0:
                        obtener_ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                        obtener_ejercicio.delete()

                        response_data = {'result': 'ok'}
                    else:
                        response_data = {'result':'fail', 'message': 'Este ejercicio no existe'}
                else:
                    response_data = {'result':'fail', 'message': 'Este usuario no tiene permisos'}
            else:
                response_data = {'result':'fail', 'message': 'Este usuario no tiene permisos'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


@csrf_exempt
def crear_clase(request):
    """
        {
        data:
            {
            "nombre":"nombre"
            "token":"token"
            }
        }
        Esta vista crea las clases a las que van unidas los usuarios.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        nombre = data.get('nombre', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            curso_existe = Cursos.objects.filter(nombre_curso=nombre)
            if curso_existe.count() > 0:
                response_data = {'result': 'fail', 'message': 'Este curso ya existe'}
            else:
                curso = Cursos(nombre_curso=nombre)
                curso.save()
                response_data = {'result': 'ok', 'message': 'Curso guardado'}
        else:
            response_data = {'result': 'fail', 'message': 'Sesion cancelada, ha iniciado sesion desde otro terminal'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


@csrf_exempt
def corregir_ejercicio(request):
    """
        {
        data:
            {
            "idcorregir":"idcorregir"
            "token":"token"
            "idejercicio":"idejercicio"
            "resultado":"resultado"
            "estado_ejercicio":"estado_ejercicio"
            "imagen_64":"imagen_64"
            "idmateria":"idmateria"
            }
        }
        Esta vista guarda en la tabla corregir los ejercicios del alumno con los datos correspondientes.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        resultado = data.get('resultado', 'null')
        imagen_64 = data.get('imagen_64', 'null')
        estado = data.get('estado_ejercicio', 'null')
        idcorregir = data.get('idcorregir', 'null')
        idmateria = data.get('idmateria', 'null')
        numero_intentos = data.get('numero_intentos', 'null')
        numero_imagenes = data.get('numero_imagenes', 'null')
        numero_preguntas = data.get('numero_preguntas', 'null')
        fallos = data.get('fallos', 'null')
        nota_auto = data.get('nota_auto', 'null')
        
        fecha = datetime.datetime.now(pytz.utc)+datetime.timedelta(0,7200)
        fecha = str(fecha)
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            materia = MateriasEjercicios.objects.get(idmateria=idmateria)
            if idcorregir != "null":
                cojer_corregir = Corregir.objects.filter(idcorregir=idcorregir)                
                if cojer_corregir.count() > 0:
                    cojer_corregir = Corregir.objects.get(idcorregir=idcorregir)
                    pendiente = EjerciciosPendientes.objects.get(idcorregir=idcorregir)
                    pendiente.delete()
                    if cojer_corregir.urlimagen != "null":
                        ruta_imagen = cojer_corregir.urlimagen
                        ruta_imagen = ruta_imagen.replace(" ","+")
                        file = open(config.ruta_imagen_konecta2 + ruta_imagen, "w")
                        image_b64 = imagen_64.replace(" ","+")
                        image_bin = base64.b64decode(image_b64)
                        file.write(image_bin)
                        file.close()
                    else:
                        if str(imagen_64) != "null":
                            ruta_imagen = config.ruta_imagen_ejercicios +idcorregir+".png"
                            ruta_imagen = ruta_imagen.replace(" ","+")
                            file = open(config.ruta_imagen_konecta2 + ruta_imagen, "w")
                            image_b64 = imagen_64.replace(" ","+")
                            image_bin = base64.b64decode(image_b64)
                            file.write(image_bin)
                            file.close()
                            cojer_corregir.urlimagen = ruta_imagen
                        else:
                            cojer_corregir.urlimagen = "null"
                        
                    obtener_ejercicios = Ejercicios.objects.get(idejercicio=idejercicio)
                    cojer_corregir.idejercicio = obtener_ejercicios
                    cojer_corregir.idusuario = cojer_usuario.userid
                    cojer_corregir.resultado = resultado
                    cojer_corregir.materia = materia
                    cojer_corregir.estado = estado
                    cojer_corregir.fecha = fecha
                    cojer_corregir.numerointentos = numero_intentos
                    cojer_corregir.numeroimagenes = numero_imagenes
                    cojer_corregir.numeropreguntas = numero_preguntas
                    cojer_corregir.fallos = fallos
                    cojer_corregir.nota = nota_auto
                    cojer_corregir.save()
                    
                    response_data = {'result':'ok', 'message':'Modificado'}
                    return HttpResponse(json.dumps(response_data), mimetype="application/json")
            else:
                response_data = {'result': 'fail', 'message':'No se encuentra el id corregir'}
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def ver_corregir_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idalumno":"idalumno"
            }
        }
        Esta vista muestra los ejercicios que el profesor tiene pendientes por corregir.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idalumno = data.get('idalumno', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            cojer_profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            response_data = {'ejercicios':[],'result':'ok'}            
            for corregir in Corregir.objects.filter(idusuario=idalumno):
                if corregir.estado != "sin hacer":
                    ejercicio = Ejercicios.objects.get(idejercicio=corregir.idejercicio.idejercicio)
                    response_data['ejercicios'].append({'titulo': ejercicio.titulo,
                        'idejercicio': ejercicio.idejercicio, 
                        'idcorregir': corregir.idcorregir, 
                        'descripcion': ejercicio.descripcion,
                        'dificultad': ejercicio.dificultad.nombre,
                        'materia': ejercicio.materia.nombre,
                        'resultado': corregir.resultado,
                        'tipo': ejercicio.tipo,
                        'urlimagen': corregir.urlimagen,
                        'interfaz': ejercicio.interfaz,
                        'fecha': corregir.fecha,
                        'estado': corregir.estado,
                        'numero_intentos': corregir.numerointentos,
                        'numero_imagenes': corregir.numeroimagenes,
                        'numero_preguntas': corregir.numeropreguntas,
                        'fallos': corregir.fallos,
                        'nota_auto': corregir.nota})

        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}


        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def ver_imagen_corregir(request):
    """
        {
        data:
            {
            "token":"token"
            "idcorregir":"idcorregir"
            }
        }
        Esta vista envia la imagen de un ejercicio de la tabla corregir
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcorregir = data.get('idcorregir', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        
        if comprobar_usuario.count() > 0:
            coger_corregir = Corregir.objects.get(idcorregir=idcorregir)
            if coger_corregir.urlimagen != "null":            
                file = open(config.ruta_imagen_konecta2 + coger_corregir.urlimagen, "r")
                imagen_bin = file.read()               
                file.close()
                image_b64 = base64.b64encode(imagen_bin)
                response_data = {'imagen':image_b64,'result':'ok'}
            else:
                response_data = {'result':'fail'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}


        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def eliminar_corregir(request):
    """
        {
        data:
            {
            "token":"token"
            "idcorregir":"idcorregir"
            }
        }
        Esta vista elimina el ejercicio a corregir del cual se mande el id.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcorregir = data.get('idcorregir', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_corregir = Corregir.objects.filter(idcorregir=idcorregir)
            if cojer_corregir.count() > 0:
                cojer_corregir = Corregir.objects.get(idcorregir=idcorregir)
                cojer_corregir.delete()
                response_data = {'result':'ok', 'message':'Eliminado'}
            else:
                response_data = {'result':'fail', 'message':'No existe el ejercicio a corregir'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")




@csrf_exempt
def modificar_curso_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idcurso":"idcurso"
            "nombre":"nombre"
            }
        }
        Esta vista modifica un curso de ejercicios"""
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcurso = data.get('idcurso', 'null')
        nombre = data.get('nombre', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_curso = CursosEjercicios.objects.filter(idcursos=idcurso)
            if comprobar_curso.count() > 0:
                cojer_curso = CursosEjercicios.objects.get(idcursos=idcurso)
                cojer_curso.nombre = nombre
                cojer_curso.save()
                response_data = {'result':'ok', 'message':'Curso modificado'}
            else:
                response_data = {'result':'fail', 'message':'Curso no encontrado'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def modificar_materia_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idmateria":"idmateria"
            "nombre":"nombre"
            }
        }
        Esta vista modifica una materia de ejercicios"""
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idmateria = data.get('idmateria', 'null')
        nombre = data.get('nombre', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_materia = MateriasEjercicios.objects.filter(idmateria=idmateria)
            if comprobar_materia.count() > 0:
                cojer_materia = MateriasEjercicios.objects.get(idmateria=idmateria)
                cojer_materia.nombre = nombre
                cojer_materia.save()
                response_data = {'result':'ok', 'message':'Materia modificada'}
            else:
                response_data = {'result':'fail', 'message':'Materia no encontrada'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def modificar_tema_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idtema":"idtema"
            "nombre":"nombre"
            }
        }
        Esta vista modifica un tema de ejercicios"""
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idtema = data.get('idmateria', 'null')
        nombre = data.get('nombre', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_tema = Tema.objects.filter(idtema=idtema)
            if comprobar_tema.count() > 0:
                cojer_tema = Tema.objects.get(idtema=idtema)
                cojer_tema.nombre = nombre
                cojer_tema.save()
                response_data = {'result':'ok', 'message':'Tema modificada'}
            else:
                response_data = {'result':'fail', 'message':'Tema no encontrado'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def eliminar_curso_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idcurso":"idcurso"
            }
        }
        Esta vista elimina un curso de ejercicios y con el las materias, temas y ejercicios relacionados.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idcurso = data.get('idcurso', 'null')

        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_curso = CursosEjercicios.objects.filter(idcursos=idcurso)
            if comprobar_curso.count() > 0:
                for ejercicio in Ejercicios.objects.filter(curso=idcurso):
                    ejercicio.delete()
                for materia in MateriasEjercicios.objects.filter(curso=idcurso):
                    for tema in Tema.objects.filter(materia=materia):
                        tema.delete()
                    materia.delete()
                cojer_curso = CursosEjercicios.objects.filter(idcursos=idcurso)
                cojer_curso.delete()
                response_data = {'result':'ok'}
            else:
                response_data = {'result':'fail', 'message':'Curso no encontrado'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def eliminar_materia_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idmateria":"idmateria"
            }
        }
        Esta vista elimina una materia de ejercicios y con el los temas y ejercicios relacionados.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idmateria = data.get('idmateria', 'null')

        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_materia = MateriasEjercicios.objects.filter(idmateria=idmateria)
            if comprobar_materia.count() > 0:
                for ejercicio in Ejercicios.objects.filter(materia=idmateria):
                    ejercicio.delete()
                for tema in Tema.objects.filter(materia=idmateria):
                    tema.delete()

                cojer_materia = MateriasEjercicios.objects.filter(idmateria=idmateria)
                cojer_materia.delete()
                response_data = {'result':'ok'}
            else:
                response_data = {'result':'fail', 'message':'Materia no encontrada'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def eliminar_tema_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idtema":"idtema"
            }
        }
        Esta vista elimina un tema de ejercicios y con el los ejercicios relacionados.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idtema = data.get('idtema', 'null')

        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_tema = Tema.objects.filter(idtema=idtema)
            if comprobar_tema.count() > 0:
                for ejercicio in Ejercicios.objects.filter(tema=idtema):
                    ejercicio.delete()
                cojer_tema = Tema.objects.filter(idtema=idtema)
                cojer_tema.delete()
                response_data = {'result':'ok'}
            else:
                response_data = {'result':'fail', 'message':'Materia no encontrada'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def detalles_usuario(request):
    """
        {
        data:
            {
            "token":"token"
            "tipo":"tipo"
            "idusuario":"idusuario"
            }
        }
        Esta vista devuelve los datos de un alumno.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        tipo = data.get('tipo', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            if tipo == "Profesores":
                usuario_existe = User.objects.filter(id=idusuario)
                if usuario_existe.count() >0:
                    usuario_existe = User.objects.get(id=idusuario)
                    profesor_existe = Profesor.objects.filter(idusuario=usuario_existe)
                    if profesor_existe.count() > 0:
                        profesor_existe = Profesor.objects.get(idusuario=usuario_existe)
                        permisos_profesor = Permisos.objects.get(idusuario=usuario_existe)
                        if str(profesor_existe.urlimagen) == "":
                            imagen = "null"
                        else:
                            imagen = profesor_existe.urlimagen
                        response_data = {'result':'ok', 
                        'nombre':profesor_existe.nombre,
                        'username':usuario_existe.username,
                        'last_login':str(usuario_existe.last_login+datetime.timedelta(0, 7200)),
                        'primer_apellido': profesor_existe.apellido1, 
                        'segundo_apellido': profesor_existe.apellido2,
                        'idusuario': profesor_existe.idusuario.id,
                        'tipo': 'Profesor',
                        'estado': profesor_existe.estado,
                        'nacimiento': profesor_existe.nacimiento,
                        'url_imagen': imagen,
                        'idusuario': profesor_existe.idusuario.id,
                        'crear_usuario': permisos_profesor.crear_usuario,
                        'ver_todos_usuarios': permisos_profesor.ver_todos_usuarios,
                        'modificar_usuario': permisos_profesor.modificar_usuario,
                        'eliminar_usuario': permisos_profesor.eliminar_usuario,
                        'ver_notas': permisos_profesor.ver_notas,
                        'modificar_notas': permisos_profesor.modificar_notas,
                        'eliminar_ejercicios': permisos_profesor.eliminar_ejercicio,
                        'crear_ejercicios': permisos_profesor.crear_ejercicio,
                        'modificar_ejercicios': permisos_profesor.modificar_ejercicio,
                        'cursos': []
                        }
                        for cursos in profesor_existe.curso.all():
                            response_data['cursos'].append({'idcurso': cursos.idcurso, 'nombre_curso': cursos.nombre_curso})
                        return HttpResponse(json.dumps(response_data), mimetype="application/json")
                    else:
                        response_data = {'result':'fail', 'message': 'El perfil del profesor no existe'}
                else:
                    response_data =  {'result':'fail', 'message': 'El usuario no existe'}
            if tipo == "Alumnos":    
                usuario_existe = User.objects.filter(id=idusuario)
                if usuario_existe.count() >0:
                    usuario_existe = User.objects.get(id=idusuario)
                    alumno_existe = Alumno.objects.filter(idusuario=usuario_existe)
                    if alumno_existe.count() > 0:
                        alumno_existe = Alumno.objects.get(idusuario=usuario_existe)
                        
                        if str(alumno_existe.urlimagen) == "":
                            imagen = "null"
                        else:
                            imagen = alumno_existe.urlimagen
                            
                        response_data = {'result':'ok', 
                        'nombre':alumno_existe.nombre,
                        'username':usuario_existe.username,
                        'last_login':str(usuario_existe.last_login+datetime.timedelta(0, 7200)), 
                        'primer_apellido': alumno_existe.apellido1, 
                        'segundo_apellido': alumno_existe.apellido2,
                        'url_imagen': imagen,
                        'nacimiento': alumno_existe.nacimiento,
                        'idusuario': alumno_existe.idusuario.id,
                        'estado': alumno_existe.estado,
                        'tipo':'Alumno',
                        'cursos': [],
                        'profesores': []
                        }
                        for cursos in alumno_existe.curso.all():
                            response_data['cursos'].append({'nombre_curso': cursos.nombre_curso})
                            for profesores in Profesor.objects.filter(curso=cursos):
                                response_data['profesores'].append({'nombre': profesores.nombre + " " + profesores.apellido1})
                                
                        return HttpResponse(json.dumps(response_data), mimetype="application/json")
                    else:
                        response_data = {'result':'fail', 'message': 'El perfil del alumno no existe'}
                        return HttpResponse(json.dumps(response_data), mimetype="application/json")
                else:
                    response_data =  {'result':'fail', 'message': 'El usuario no existe'}
                    return HttpResponse(json.dumps(response_data), mimetype="application/json")
            else:
                    response_data =  {'result':'fail', 'message': 'Tipo no encontrado'}
                    return HttpResponse(json.dumps(response_data), mimetype="application/json")
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
            

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def guardar_incidencia(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            "comentario":"comentario"
            }
        }
        Esta vista guarda / modifica una incidencia
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        comentario = data.get('comentario', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_incidencia = Incidencias.objects.filter(idusuario=idusuario)
            if comprobar_incidencia.count() > 0:
                comprobar_incidencia = Incidencias.objects.get(idusuario=idusuario)
                comprobar_incidencia.comentario = comentario
                comprobar_incidencia.save()
                response_data = {'result':'ok'}
            else:
                usuario = User.objects.get(id=idusuario)
                incidencia_nueva = Incidencias(idusuario=usuario, comentario=comentario)
                incidencia_nueva.save()
                response_data = {'result':'ok'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def guardar_observacion(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            "comentario":"comentario"
            }
        }
        Esta vista guarda una observacion de un usuario.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        comentario = data.get('comentario', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_observacion = Observaciones.objects.filter(idusuario=idusuario)
            if comprobar_observacion.count() > 0:
                comprobar_observacion = Observaciones.objects.get(idusuario=idusuario)
                comprobar_observacion.comentario = comentario
                comprobar_observacion.save()
                response_data = {'result':'ok'}
            else:
                usuario = User.objects.get(id=idusuario)
                observacion_nueva = Observaciones(idusuario=usuario, comentario=comentario)
                observacion_nueva.save()
                response_data = {'result':'ok'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def ver_observacion(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            }
        }
        Esta vistamuestra una observacion de un usuario.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_observacion = Observaciones.objects.filter(idusuario=idusuario)
            if comprobar_observacion.count() > 0:
                comprobar_observacion = Observaciones.objects.get(idusuario=idusuario)
                response_data = {'result':'ok', 'comentario': comprobar_observacion.comentario}
            else:
                response_data = {'result':'fail'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def ver_incidencia(request):
    """
        {
        data:
            {
            "token":"token"
            "idusuario":"idusuario"
            }
        }
        Esta vista muestra una incidencia de un alumno.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idusuario = data.get('idusuario', 'null')
        
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            comprobar_incidencia = Incidencias.objects.filter(idusuario=idusuario)
            if comprobar_incidencia.count() > 0:
                comprobar_incidencia = Incidencias.objects.get(idusuario=idusuario)
                response_data = {'result':'ok', 'comentario': comprobar_incidencia.comentario}
            else:
                response_data = {'result':'fail'}
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def materias_totales_java(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        Esta vista muestra todas las materias.
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            response_data = {'materias': []}
            for materia in MateriasEjercicios.objects.all():
                response_data['materias'].append({'nombre': materia.nombre, 'idmateria': materia.idmateria})
        else:
            response_data = {'result':'fail', 'message':'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")    
    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def detalles_ejercicio_profesor(request):
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
            
            comprobar_ejercicio = Ejercicios.objects.filter(idejercicio=idejercicio)
            if comprobar_ejercicio.count() > 0:
                obtener_ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                response_data = {'result': 'ok', 'titulo': obtener_ejercicio.titulo, 'descripcion': obtener_ejercicio.descripcion, 'idejercicio': obtener_ejercicio.idejercicio, 'imagen': obtener_ejercicio.imagen, 'calculadora': obtener_ejercicio.calculadora, 'dificultad': obtener_ejercicio.dificultad.nombre, 'interfaz':  obtener_ejercicio.interfaz, 'consejo': obtener_ejercicio.consejo}
            else:
                response_data = {'result':'fail', 'message': 'Ejercicio no encontrado'}
            
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def reenviar_ejercicio(request):
    """
        {
        data:
            {
            "token":"token"
            "idejercicio":"idejercicio"
            "idcorregir":"idcorregir"
            "idalumno":"idalumno"
            }
        }
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        idejercicio = data.get('idejercicio', 'null')
        idalumno = data.get('idalumno', 'null')
        idcorregir = data.get('idcorregir', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)

        if comprobar_usuario.count() > 0:
            token_usuario = Tokenregister.objects.get(token=token)
            comprobar_profesor = Profesor.objects.filter(idusuario=token_usuario.userid.id)
            if comprobar_profesor.count() > 0:
                obtener_profesor = Profesor.objects.get(idusuario=token_usuario.userid.id)
                obtener_usuario = User.objects.filter(id=idalumno)
                if obtener_usuario.count() > 0:
                    obtener_usuario = User.objects.get(id=idalumno)
                    obtener_ejercicio = Ejercicios.objects.filter(idejercicio=idejercicio)
                    if obtener_ejercicio.count() > 0:
                        fecha = datetime.datetime.now(pytz.utc)+datetime.timedelta(0,7200)
                        fecha = str(fecha)
                        obtener_ejercicio = Ejercicios.objects.get(idejercicio=idejercicio)
                        ejercicio_pendiente = EjerciciosPendientes(idprofesor=obtener_profesor, idcorregir=idcorregir, idejercicio=obtener_ejercicio, idalumno=obtener_usuario, fecha=fecha)
                        ejercicio_pendiente.save()
                        response_data = {'result':'ok', 'message': 'Reenviado correctamente'}
                    else:
                        response_data = {'result':'fail', 'message': 'Ejercicio no encontrado'}
                else:
                    response_data = {'result':'fail', 'message': 'Usuario no encontrado'}
            else:
                response_data = {'result':'fail', 'message': 'El user no es un profesor'}
        else:
            response_data = {'result':'fail', 'message': 'Token no encontrado'}

        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
"""
-------------------------------Gestion de ejercicios Android-----------------------------------------------------------
"""
@csrf_exempt
def ejercicios_normales(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            response_data = {'ejercicios':[]}
            for tema in Tema.objects.filter(tipo="publico"):
                for ejercicio in Ejercicios.objects.filter(tema=tema):
                    usuario_profesor = User.objects.get(id=ejercicio.idprofesor.id)
                    profesor = Profesor.objects.get(idusuario=usuario_profesor)
                    response_data['ejercicios'].append({'profesor':profesor.nombre, 'idejercicio': ejercicio.idejercicio,
                                                        'titulo':ejercicio.titulo, 'imagen':ejercicio.imagen, 
                                                        'descripcion':ejercicio.descripcion, 'materia':ejercicio.materia.nombre,
                                                        'curso': ejercicio.curso.nombre, 'dificultad': ejercicio.dificultad.nombre,
                                                        'tema': ejercicio.tema.nombre, 'resultado':ejercicio.resultado, 
                                                        'calculadora':ejercicio.calculadora, 'interfaz': ejercicio.interfaz, 
                                                        'consejo': ejercicio.consejo, 'tipo': ejercicio.tipo})
            for tema in Tema.objects.filter(tipo=cojer_usuario.userid.id):
                for ejercicio in Ejercicios.objects.filter(tema=tema):
                    usuario_profesor = User.objects.get(id=ejercicio.idprofesor.id)
                    profesor = Profesor.objects.get(idusuario=usuario_profesor)
                    response_data['ejercicios'].append({'profesor':profesor.nombre, 'idejercicio': ejercicio.idejercicio,
                                                        'titulo':ejercicio.titulo, 'imagen':ejercicio.imagen, 
                                                        'descripcion':ejercicio.descripcion, 'materia':ejercicio.materia.nombre,
                                                        'curso': ejercicio.curso.nombre, 'dificultad': ejercicio.dificultad.nombre,
                                                        'tema': ejercicio.tema.nombre, 'resultado':ejercicio.resultado, 
                                                        'calculadora':ejercicio.calculadora, 'interfaz': ejercicio.interfaz, 
                                                        'consejo': ejercicio.consejo, 'tipo': ejercicio.tipo})
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def ejercicios_clase(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            response_data = {'ejercicios':[]}
            permisos = Permisos.objects.get(idusuario=cojer_usuario.userid)
            profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            if permisos.ver_notas == 1:
                for ejercicio in EjerciciosClase.objects.all():
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idejercicioclase':ejercicio.idejercicioclase, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
            else:
                for ejercicio in EjerciciosClase.objects.filter(idprofesor=profesor):
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idejercicioclase':ejercicio.idejercicioclase, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def controles(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            response_data = {'ejercicios':[]}
            permisos = Permisos.objects.get(idusuario=cojer_usuario.userid)
            profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            if permisos.ver_notas == 1:
                for ejercicio in Controles.objects.all():
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idcontroles':ejercicio.idcontroles, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
            else:
                for ejercicio in Controles.objects.filter(idprofesor=profesor):
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idcontroles':ejercicio.idcontroles, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def examenes(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            response_data = {'ejercicios':[]}
            permisos = Permisos.objects.get(idusuario=cojer_usuario.userid)
            profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            if permisos.ver_notas == 1:
                for ejercicio in Examenes.objects.all():
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idexamenes':ejercicio.idejecamenes, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
            else:
                for ejercicio in Examenes.objects.filter(idprofesor=profesor):
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idexamenes':ejercicio.idejecamenes, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
@csrf_exempt
def globales(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            response_data = {'ejercicios':[]}
            permisos = Permisos.objects.get(idusuario=cojer_usuario.userid)
            profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            if permisos.ver_notas == 1:
                for ejercicio in Globales.objects.all():
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idglobales':ejercicio.idglobales, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
            else:
                for ejercicio in Globales.objects.filter(idprofesor=profesor):
                    alumno = Alumno.objects.get(idusuario=ejercicio.idusuario)
                    response_data['ejercicios'].append({'idglobales':ejercicio.idglobales, 'idejercicio': ejercicio.idejercicio.idejercicio,
                                                        'fecha': ejercicio.fecha, 'idusuario': ejercicio.idusuario.id,
                                                        'idcurso': ejercicio.idclase.idcurso, 'imagen': ejercicio.imagen,
                                                        'nota': ejercicio.nota, 'booleano': ejercicio.booleano,
                                                        'resultado_alumno': ejercicio.resultado, 'tiemporealizacion': ejercicio.tiemporealizacion,
                                                        'intentos': ejercicio.intentos, 'titulo': ejercicio.idejercicio.titulo,
                                                        'imagen_ejercicio': ejercicio.idejercicio.titulo, 'descripcion': ejercicio.idejercicio.descripcion,
                                                        'materia': ejercicio.idejercicio.materia.nombre, 'curso': ejercicio.idejercicio.curso.nombre, 
                                                        'dificultad': ejercicio.idejercicio.dificultad.nombre, 'tema': ejercicio.idejercicio.tema.nombre,
                                                        'interfaz': ejercicio.idejercicio.interfaz, 'nombre_completo': alumno.nombre + " "+ alumno.apellido1+ " " + alumno.apellido2})
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

@csrf_exempt
def corregir(request):
    """
        {
        data:
            {
            "token":"token"
            }
        }
        
    """
    try:
        data = json.loads(request.POST['data'])
        token = data.get('token', 'null')
        comprobar_usuario = Tokenregister.objects.filter(token=token)
        if comprobar_usuario.count() > 0:
            cojer_usuario = Tokenregister.objects.get(token=token)
            profesor = Profesor.objects.get(idusuario=cojer_usuario.userid)
            response_data = {'ejercicios':[]}
            for curso in profesor.curso.all():
                for alumno in Alumno.objects.filter(curso=curso):
                    for corregir in Corregir.objects.filter(idusuario=alumno.idusuario.id):
                        if corregir.estado != "sin hacer":
                            ejercicio = Ejercicios.objects.get(idejercicio=corregir.idejercicio.idejercicio)
                            response_data['ejercicios'].append({'titulo': ejercicio.titulo,
                                'idejercicio': ejercicio.idejercicio, 
                                'idcorregir': corregir.idcorregir, 
                                'descripcion': ejercicio.descripcion,
                                'dificultad': ejercicio.dificultad.nombre,
                                'materia': ejercicio.materia.nombre,
                                'resultado': corregir.resultado,
                                'tipo': ejercicio.tipo,
                                'urlimagen': corregir.urlimagen,
                                'interfaz': ejercicio.interfaz,
                                'fecha': corregir.fecha,
                                'estado': corregir.estado,
                                'numero_intentos': corregir.numerointentos,
                                'numero_imagenes': corregir.numeroimagenes,
                                'numero_preguntas': corregir.numeropreguntas,
                                'fallos': corregir.fallos,
                                'nota_auto': corregir.nota})
        else:
            response_data = {'result': 'fail', 'message': 'Token no encontrado'}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    except BaseException, e:
        response_data = {'errorcode': 'E000', 'result': 'fail', 'message': e.message}
        return HttpResponse(json.dumps(response_data), mimetype="application/json")


