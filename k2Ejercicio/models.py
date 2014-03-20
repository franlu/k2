# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from k2Usuario.models import Alumno, Profesor


class Curso(models.Model):
    """
        Agrupar ejercicios
    """
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Cursos"

    def __unicode__(self):
        return u"%s" % self.nombre

class Materia(models.Model):
    curso = models.ForeignKey(Curso)
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Materias"

    def __unicode__(self):
        return u"%s" % self.nombre

class Tema(models.Model):
    materia = models.ForeignKey(Materia)
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20) #Publico Privado ...

    def __unicode__(self):
        return u"%s" % self.nombre

class Dificultad(models.Model):
    nombre = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = "Dificultades"

    def __unicode__(self):
        return u"%s" % self.nombre


class TipoEjercicio(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Tipo de ejercicios"

    def __unicode__(self):
        return u"%s" % self.nombre


class Ejercicio(models.Model):
    profesor = models.ForeignKey(Profesor)
    curso = models.ForeignKey(Curso)
    materia = models.ForeignKey(Materia)
    tema = models.ForeignKey(Tema)
    dificultad = models.ForeignKey(Dificultad)
    tipo = models.ForeignKey(TipoEjercicio)
    centro = models.CharField(max_length=10, blank=True)
    titulo = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=3000)
    herramientas = models.CharField(max_length=200)


    class Meta:
        verbose_name_plural = "Ejercicios"

    def __unicode__(self):
        return u"%s" % self.titulo


class Notificacion(models.Model):
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=50)
    mensaje = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Notificaciones"

    def __unicode__(self):
        return u"%s" % self.usuario

class Incidencias(models.Model):
    usuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000, unique=True)

    class Meta:
        verbose_name_plural = "Incidencias"

    def __unicode__(self):
        return u"%s" % self.usuario


class Observaciones(models.Model):
    usuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000, unique=True)

    class Meta:
        verbose_name_plural = "Observaciones"

    def __unicode__(self):
        return u"%s" % self.usuario


class EstadoEjercicios(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Estado de ejercicios"

    def __unicode__(self):
        return u"%s" % self.nombre


class ExamenManager(models.Manager):
    def get_queryset(self):
        return super(ExamenManager, self).get_queryset().filter(tipoejercicio=1)


class ControlManager(models.Manager):
    def get_queryset(self):
        return super(ControlManager, self).get_queryset().filter(tipoejercicio=2)


class EjercicioClaseManager(models.Manager):
    def get_queryset(self):
        return super(EjercicioClaseManager, self).get_queryset().filter(tipoejercicio=3)


class GlobalManager(models.Manager):
    def get_queryset(self):
        return super(GlobalManager, self).get_queryset().filter(tipoejercicio=4)


class EjercicioEnviado(models.Model):
    ejercicio = models.ForeignKey(Ejercicio)
    profesor = models.ForeignKey(Profesor)
    alumno = models.ForeignKey(Alumno)
    curso = models.ForeignKey(Curso)
    tipoejercicio = models.ForeignKey(TipoEjercicio)
    materia = models.ForeignKey(Materia)
    estadoejercicio = models.ForeignKey(EstadoEjercicios)
    fecha_envio = models.DateTimeField()
    fecha_recibido = models.DateTimeField(null=True, blank=True)
    nota = models.CharField(max_length=10, null=True, blank=True)
    bien_mal = models.BooleanField(blank=True)
    tiempo_realizacion = models.IntegerField(null=True, blank=True, default=0)
    tiempo_maximo = models.IntegerField(null=True, blank=True, default=0)
    intentos_posibles = models.IntegerField(null=True, blank=True, default=0)
    intentos_realizados = models.IntegerField(null=True, blank=True, default=0)
    nfallos = models.IntegerField(null=True, blank=True, default=0)

    objects = models.Manager()
    examenes = ExamenManager()  # 1
    controles = ControlManager()  # 2
    ejerciciosclase = EjercicioClaseManager()  # 3
    globales = GlobalManager()  # 4

    class Meta:
        verbose_name_plural = "Todos los ejercicios"

    def __unicode__(self):
        return u"%s" % self.id


class Pregunta(models.Model):
    enunciado = models.CharField(max_length=2000, null=True, blank=True)
    respuesta = models.CharField(max_length=2000, null=True, blank=True)
    consejo = models.CharField(max_length=2000, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.id
