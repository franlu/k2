# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from django.forms import ModelForm
#from django.db.models.signals import post_save
import os

"""cursos - cambiar por clases
 usuario de django profesor y alumno
ojo con los permisos  / tabla
curso ejercicios
materias
temas
dificultad
Ejercicio
Ejercicios pendientes alumno """

PROJECT_PATH = os.path.dirname("__file__")


class Permisos(models.Model):
    idusuario = models.ForeignKey(User)
    crear_usuario = models.CharField(max_length=5)
    ver_todos_usuarios = models.CharField(max_length=5)
    modificar_usuario = models.CharField(max_length=5)
    eliminar_usuario = models.CharField(max_length=5)
    ver_notas = models.CharField(max_length=5)
    modificar_notas = models.CharField(max_length=5)
    crear_ejercicio = models.CharField(max_length=5)
    modificar_ejercicio = models.CharField(max_length=5)
    eliminar_ejercicio = models.CharField(max_length=5)

    def __unicode__(self):
        return u"%s" % self.idusuario


class Tokenregister(models.Model):
    tokenid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    token = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.tokenid


class Cursos(models.Model):
    idcurso = models.AutoField(primary_key=True)
    nombre_curso = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.nombre_curso


class Invitado(models.Model):
    idusuario = models.ForeignKey(User)
    curso = models.ManyToManyField(Cursos)
    nombre = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s" % self.nombre


class Profesor(models.Model):
    idusuario = models.ForeignKey(User)
    curso = models.ManyToManyField(Cursos)
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=20)
    urlimagen = models.CharField(max_length=200)
    nacimiento = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % self.nombre


class Alumno(models.Model):
    idusuario = models.ForeignKey(User)
    curso = models.ManyToManyField(Cursos)
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=20)
    urlimagen = models.CharField(max_length=200)
    nacimiento = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % self.nombre


class CursosEjercicios(models.Model):
    idcursos = models.AutoField(primary_key=True)
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.nombre


class MateriasEjercicios(models.Model):
    idmateria = models.AutoField(primary_key=True)
    curso = models.ForeignKey(CursosEjercicios)
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.nombre


class Tema(models.Model):
    idtema = models.AutoField(primary_key=True)
    materia = models.ForeignKey(MateriasEjercicios)
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.nombre


class Dificultad(models.Model):
    iddificultad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.nombre

class TiposEjercicios(models.Model):
    idtipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.nombre


class Ejercicios(models.Model):
    idejercicio = models.AutoField(primary_key=True)
    idprofesor = models.ForeignKey(Profesor)
    curso = models.ForeignKey(CursosEjercicios)
    materia = models.ForeignKey(MateriasEjercicios)
    tema = models.ForeignKey(Tema)
    dificultad = models.ForeignKey(Dificultad)
    tipo = models.ForeignKey(TiposEjercicios)
    idcentro = models.CharField(max_length=500)
    titulo = models.CharField(max_length=500)
    imagen = models.CharField(max_length=500)
    descripcion = models.CharField(max_length=3000)
    resultado = models.CharField(max_length=500, null=True, blank=True)
    calculadora = models.CharField(max_length=1)
    interfaz = models.CharField(max_length=200)
    consejo = models.CharField(max_length=200)
    estado = models.CharField(max_length=200, null=True, blank=True)


    def __unicode__(self):
        return u"%s" % self.titulo


class Notificacion(models.Model):
    idnotificacion = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(User)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=200)
    mensaje = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.idusuario

"""
class EjerciciosClase(models.Model):
    idejercicioclase = models.AutoField(primary_key=True)
    idejercicio = models.ForeignKey(Ejercicios)
    idusuario = models.ForeignKey(User)
    idprofesor = models.ForeignKey(Profesor)
    idclase = models.ForeignKey(Cursos)
    fecha = models.DateTimeField()
    imagen = models.CharField(max_length=500)
    nota = models.CharField(max_length=10, null=True, blank=True)
    booleano = models.CharField(max_length=10, null=True, blank=True)
    resultado = models.CharField(max_length=500)
    tiemporealizacion = models.CharField(max_length=100)
    intentos = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.idusuario


class Controles(models.Model):
    idcontroles = models.AutoField(primary_key=True)
    idejercicio = models.ForeignKey(Ejercicios)
    idusuario = models.ForeignKey(User)
    idprofesor = models.ForeignKey(Profesor)
    idclasem = models.ForeignKey(Cursos)
    fecha = models.DateTimeField()
    imagen = models.CharField(max_length=500)
    nota = models.CharField(max_length=10, null=True, blank=True)
    booleano = models.CharField(max_length=10, null=True, blank=True)
    resultado = models.CharField(max_length=500)
    tiemporealizacion = models.CharField(max_length=100)
    intentos = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.idusuario


class Examenes(models.Model):
    idexamen = models.AutoField(primary_key=True)
    idejercicio = models.ForeignKey(Ejercicios)
    idusuario = models.ForeignKey(User)
    idprofesor = models.ForeignKey(Profesor)
    idclase = models.ForeignKey(Cursos)
    fecha = models.DateTimeField(max_length=100)
    imagen = models.CharField(max_length=500)
    nota = models.CharField(max_length=10, null=True, blank=True)
    booleano = models.CharField(max_length=10, null=True, blank=True)
    resultado = models.CharField(max_length=500)
    tiemporealizacion = models.CharField(max_length=100)
    intentos = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.idusuario


class Globales(models.Model):
    idglobales = models.AutoField(primary_key=True)
    idejercicio = models.ForeignKey(Ejercicios)
    idusuario = models.ForeignKey(User)
    idprofesor = models.ForeignKey(Profesor)
    idclase = models.ForeignKey(Cursos)
    fecha = models.DateTimeField(max_length=100)
    imagen = models.CharField(max_length=500)
    nota = models.CharField(max_length=10, null=True, blank=True)
    booleano = models.CharField(max_length=10, null=True, blank=True)
    resultado = models.CharField(max_length=500)
    tiemporealizacion = models.CharField(max_length=100)
    intentos = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.idusuario
"""

class Corregir(models.Model):
    idcorregir = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(User)
    idejercicio = models.ForeignKey(Ejercicios)
    materia = models.ForeignKey(MateriasEjercicios)
    resultado = models.CharField(max_length=500)
    urlimagen = models.CharField(max_length=500)
    estado = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    numerointentos = models.CharField(max_length=100)
    numeroimagenes = models.CharField(max_length=100)
    numeropreguntas = models.CharField(max_length=100)
    fallos = models.CharField(max_length=100)
    nota = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.idusuario


class EjerciciosPendientes(models.Model):
    idpendientes = models.AutoField(primary_key=True)
    idprofesor = models.ForeignKey(Profesor)
    idejercicio = models.ForeignKey(Ejercicios)
    idalumno = models.ForeignKey(User)
    idcorregir = models.ForeignKey(Corregir)
    fecha = models.DateTimeField()

    def __unicode__(self):
        return u"%s" % self.idpendientes


class Incidencias(models.Model):
    idusuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000)

    def __unicode__(self):
        return u"%s" % self.idusuario


class Observaciones(models.Model):
    idusuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000)

    def __unicode__(self):
        return u"%s" % self.idusuario





class EstadoEjercicios(models.Model):
    idestado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.nombre


class ExamenesManager(models.Manager):
    def get_queryset(self):
        return super(ExamenesManager, self).get_queryset().filter(idtipoejercicios=1)


class ControlesManager(models.Manager):
    def get_queryset(self):
        return super(ControlesManager, self).get_queryset().filter(idtipoejercicios=2)


class EjerciciosClaseManager(models.Manager):
    def get_queryset(self):
        return super(EjerciciosClaseManager, self).get_queryset().filter(idtipoejercicios=3)


class GlobalesManager(models.Manager):
    def get_queryset(self):
        return super(GlobalesManager, self).get_queryset().filter(idtipoejercicios=4)


class EjerciciosAll(models.Model):
    idejerciciosall = models.AutoField(primary_key=True)
    idejercicio = models.ForeignKey(Ejercicios)
    idprofesor = models.ForeignKey(Profesor)
    idalumno = models.ForeignKey(Alumno)
    idclase = models.ForeignKey(Cursos)
    idtipoejercicios = models.ForeignKey(TiposEjercicios)
    materia = models.ForeignKey(MateriasEjercicios)
    idestadoejercicio = models.ForeignKey(EstadoEjercicios)
    fecha_envio = models.DateTimeField()
    fecha_recibido = models.DateTimeField(null=True, blank=True)
    imagen_alumno = models.CharField(max_length=500, null=True, blank=True)
    imagen_profesor = models.CharField(max_length=500, null=True, blank=True)
    nota = models.CharField(max_length=10, null=True, blank=True)
    bien_mal = models.CharField(max_length=10, null=True, blank=True)
    resultado = models.CharField(max_length=500, null=True, blank=True)
    tiempo_realizacion = models.IntegerField(null=True, blank=True, default=0)
    tiempo_maximo = models.IntegerField(null=True, blank=True, default=0)
    intentos_posibles = models.IntegerField(null=True, blank=True, default=0)
    estado = models.CharField(max_length=500, null=True, blank=True)
    numerointentos = models.IntegerField(null=True, blank=True, default=0)
    numeroimagenes = models.IntegerField(null=True, blank=True, default=0)
    numeropreguntas = models.IntegerField(null=True, blank=True, default=0)
    nfallos = models.IntegerField(null=True, blank=True, default=0)

    objects = models.Manager()
    examenes = ExamenesManager() #1
    controles = ControlesManager()#2
    ejerciciosclase = EjerciciosClaseManager()#3
    globales = GlobalesManager()#4

    def __unicode__(self):
        return u"%s" % self.idejerciciosall