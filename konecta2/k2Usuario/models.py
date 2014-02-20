# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Tokenregister(models.Model):
    tokenid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    token = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.tokenid


class Clase(models.Model):
    idcurso = models.AutoField(primary_key=True)
    nombre_clase = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Clases"

    def __unicode__(self):
        return u"%s" % self.nombre_clase


class Profesor(models.Model):
    idusuario = models.ForeignKey(User, unique=True)
    clases = models.ManyToManyField(Clase)
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=20)
    urlimagen = models.ImageField(null=False, upload_to='K2Usuario/profesor/avatar/', max_length=24576)
    nacimiento = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Profesores"

    def __unicode__(self):
        return u"%s" % self.nombre


class Alumno(models.Model):
    idusuario = models.ForeignKey(User, unique=True)
    clases = models.ManyToManyField(Clase)#Foreingkey clase
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=20)
    avatar = models.ImageField(null=True, upload_to='K2Usuario/alumno/avatar/', max_length=24576)
    nacimiento = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Alumnos"

    def __unicode__(self):
        return u"%s" % self.nombre