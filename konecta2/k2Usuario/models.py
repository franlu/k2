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
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Clases"

    def __unicode__(self):
        return u"%s" % self.nombre


class Profesor(models.Model):
    idusuario = models.ForeignKey(User, unique=True)
    clases = models.ManyToManyField(Clase)
    avatar = models.ImageField(null=False, upload_to='K2Usuario/profesor/avatar/', max_length=24576)
    estado = models.CharField(max_length=20)
    nacimiento = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Profesores"

    def set_session_key(self, key):
        if self.last_session_key and not self.last_session_key == key:
            Session.objects.get(session_key=self.last_session_key).delete()
        self.last_session_key = key
        self.save()

    def __unicode__(self):
        return u"%s" % self.first_name


class Alumno(models.Model):
    idusuario = models.ForeignKey(User, unique=True)
    clase = models.ForeignKey(Clase)
    avatar = models.ImageField(null=True, upload_to='K2Usuario/alumno/avatar/', max_length=24576)
    estado = models.CharField(max_length=20)
    nacimiento = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Alumnos"


    def set_session_key(self, key):
        if self.last_session_key and not self.last_session_key == key:
            Session.objects.get(session_key=self.last_session_key).delete()
        self.last_session_key = key
        self.save()


    def __unicode__(self):
        return u"%s" % self.first_name