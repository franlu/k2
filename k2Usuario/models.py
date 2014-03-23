# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models


class Tokenregister(models.Model):
    tokenid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User)
    token = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % self.tokenid

class Clase(models.Model):
    """
        Agrupar alumnos
    """
    nombre = models.CharField(max_length=30,unique=True)

    class Meta:
        verbose_name_plural = "Clases"

    def __unicode__(self):
        return u"%s" % self.nombre


class Profesor(models.Model):
    idusuario = models.ForeignKey(User, unique=True)
    clases = models.ManyToManyField(Clase)
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20)
    avatar = models.ImageField(null=False, upload_to='k2Usuario/profesor/avatar/', max_length=24576)
    estado = models.CharField(max_length=15,default='Desconectado')
    nacimiento = models.DateField()

    class Meta:
        verbose_name_plural = "Profesores"

    def __unicode__(self):
        return u"%s" % self.idusuario


class Alumno(models.Model):
    idusuario = models.ForeignKey(User, unique=True)
    clase = models.ForeignKey(Clase)
    nombre = models.CharField(max_length=20)
    apellido1 = models.CharField(max_length=20)
    apellido2 = models.CharField(max_length=20)
    nacimiento = models.DateField()
    estado = models.CharField(max_length=15,default='Desconectado')
    avatar = models.ImageField(null=True, upload_to='k2Usuario/alumno/avatar/', max_length=24576)

    class Meta:
        verbose_name_plural = "Alumnos"

    def __unicode__(self):
        return u"%s" % self.idusuario