# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from k2Usuario.models import Alumno, Profesor, Cursos


class CursosEjercicios(models.Model):
    idcursos = models.AutoField(primary_key=True)
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "CursosEjercicios"

    def __unicode__(self):
        return u"%s" % self.nombre


class MateriasEjercicios(models.Model):
    idmateria = models.AutoField(primary_key=True)
    curso = models.ForeignKey(CursosEjercicios)
    favorito = models.ManyToManyField(User)
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Materias de ejercicios"

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

    class Meta:
        verbose_name_plural = "Dificultades"

    def __unicode__(self):
        return u"%s" % self.nombre


class TiposEjercicios(models.Model):
    idtipo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Tipo de ejercicios"

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

    class Meta:
        verbose_name_plural = "Ejercicios"

    def __unicode__(self):
        return u"%s" % self.titulo


class Notificacion(models.Model):
    idnotificacion = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(User)
    fecha = models.DateTimeField()
    tipo = models.CharField(max_length=200)
    mensaje = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Notificaciones"

    def __unicode__(self):
        return u"%s" % self.idusuario


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

    class Meta:
        verbose_name_plural = "Corregir"

    def __unicode__(self):
        return u"%s" % self.idusuario


class EjerciciosPendientes(models.Model):
    idpendientes = models.AutoField(primary_key=True)
    idprofesor = models.ForeignKey(Profesor)
    idejercicio = models.ForeignKey(Ejercicios)
    idalumno = models.ForeignKey(User)
    idcorregir = models.ForeignKey(Corregir)
    fecha = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Ejercicios pendientes"

    def __unicode__(self):
        return u"%s" % self.idpendientes


class Incidencias(models.Model):
    idusuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000)

    class Meta:
        verbose_name_plural = "Incidencias"

    def __unicode__(self):
        return u"%s" % self.idusuario


class Observaciones(models.Model):
    idusuario = models.ForeignKey(User)
    comentario = models.CharField(max_length=2000)

    class Meta:
        verbose_name_plural = "Observaciones"

    def __unicode__(self):
        return u"%s" % self.idusuario


class EstadoEjercicios(models.Model):
    idestado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

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
    examenes = ExamenesManager()  # 1
    controles = ControlesManager()  # 2
    ejerciciosclase = EjerciciosClaseManager()  # 3
    globales = GlobalesManager()  # 4

    class Meta:
        verbose_name_plural = "Todos los ejercicios"

    def __unicode__(self):
        return u"%s" % self.idejerciciosall