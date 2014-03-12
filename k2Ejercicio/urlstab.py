#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'^cursos_ejercicios/$', 'k2Ejercicio.viewstab.cursos_ejercicios'),
    (r'^materias_ejercicios/$', 'k2Ejercicio.viewstab.materias_ejercicios'),
    (r'^temas_ejercicios/$', 'k2Ejercicio.viewstab.temas_ejercicios'),
    (r'^dificultad_ejercicios/$', 'k2Ejercicio.viewstab.dificultad_ejercicios'),




 )