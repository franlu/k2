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
    nombre = models.CharField(max_length=30, unique=True)

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
    centro = models.CharField(max_length=10)
    titulo = models.CharField(max_length=50)
    imagen = models.ImageField(null=False, upload_to='k2Ejercicio/img/', max_length=24576)
    descripcion = models.CharField(max_length=3000)
    resultado = models.CharField(max_length=500, null=True, blank=True)
    calculadora = models.CharField(max_length=1)
    interfaz = models.CharField(max_length=50)
    consejo = models.CharField(max_length=200)
    estado = models.CharField(max_length=30, null=True, blank=True)

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
        return u"%s" % self.idusuario

"""
class Corregir(models.Model):
    idcorregir = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(User)
    idejercicio = models.ForeignKey(Ejercicio)
    materia = models.ForeignKey(Materia)
    resultado = models.CharField(max_length=500)
    urlimagen = models.CharField(max_length=500)
    estado = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    numerointentos = models.CharField(max_length=100)
    numeroimagenes = models.CharField(max_length=100)
    numeropreguntas = models.CharField(max_length=100)
    fallos = models.CharField(max_length=100)
    nota = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Corregir"

    def __unicode__(self):
        return u"%s" % self.idusuario


class EjerciciosPendientes(models.Model):
    idpendientes = models.AutoField(primary_key=True)
    idprofesor = models.ForeignKey(Profesor)
    idejercicio = models.ForeignKey(Ejercicio)
    idalumno = models.ForeignKey(User)
    idcorregir = models.ForeignKey(Corregir)
    fecha = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Ejercicios pendientes"

    def __unicode__(self):
        return u"%s" % self.idpendientes
"""

class Incidencias(models.Model):
    usuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000, unique=True)

    class Meta:
        verbose_name_plural = "Incidencias"

    def __unicode__(self):
        return u"%s" % self.idusuario


class Observaciones(models.Model):
    usuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000, unique=True)

    class Meta:
        verbose_name_plural = "Observaciones"

    def __unicode__(self):
        return u"%s" % self.idusuario


class EstadoEjercicios(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Estado de ejercicios"

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
    idejercicio = models.ForeignKey(Ejercicio)
    idprofesor = models.ForeignKey(Profesor)
    idalumno = models.ForeignKey(Alumno)
    idclase = models.ForeignKey(Curso)
    idtipoejercicios = models.ForeignKey(TipoEjercicio)
    materia = models.ForeignKey(Materia)
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
    examenes = ExamenesManager()  # 1
    controles = ControlesManager()  # 2
    ejerciciosclase = EjerciciosClaseManager()  # 3
    globales = GlobalesManager()  # 4

    class Meta:
        verbose_name_plural = "Todos los ejercicios"

    def __unicode__(self):
        return u"%s" % self.idejerciciosall
