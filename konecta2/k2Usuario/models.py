# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


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

    class Meta:
        verbose_name_plural = "Cursos"

    def __unicode__(self):
        return u"%s" % self.nombre_curso


class Profesor(models.Model):
    idusuario = models.ForeignKey(User)
    curso = models.ManyToManyField(Cursos)
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=20)
    urlimagen = models.CharField(max_length=200)
    nacimiento = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Profesores"

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

    class Meta:
        verbose_name_plural = "Alumnos"

    def __unicode__(self):
        return u"%s" % self.nombre