#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',

    #urls del profesor
    (r'^cursos_ejercicios/$', 'k2Ejercicio.viewstab.cursos_ejercicios'),
    (r'^materias_ejercicios/$', 'k2Ejercicio.viewstab.materias_ejercicios'),
    (r'^temas_ejercicios/$', 'k2Ejercicio.viewstab.temas_ejercicios'),
    (r'^dificultad_ejercicios/$', 'k2Ejercicio.viewstab.dificultad_ejercicios'),
    (r'^ejercicios_totales/$', 'k2Ejercicio.viewstab.ejercicios_totales'),
    (r'^detalles_ejercicio/$', 'k2Ejercicio.viewstab.detalles_ejercicio'),

    (r'^favorito_crear/$', 'k2Ejercicio.viewstab.favorito_crear'),
    (r'^favorito_borrar/$', 'k2Ejercicio.viewstab.favorito_borrar'),

    (r'^enviar_ejercicio_individual/$', 'k2Ejercicio.viewstab.enviar_ejercicio_individual'),

    #urls de ambos, aunque estan en el archivo del profesor
    (r'^consultar_notificacion/$', 'k2Ejercicio.viewstab.consultar_notificacion'),
    (r'^crear_notificacion/$', 'k2Ejercicio.viewstab.crear_notificacion'),
    (r'^borrar_notificacion/$', 'k2Ejercicio.viewstab.borrar_notificacion'),

    #urls para el alumno
    (r'^ejercicios_pendientes/$', 'k2Ejercicio.viewstab_alumno.ejercicios_pendientes'),
    (r'^getpregunta/$', 'k2Ejercicio.viewstab_alumno.getpregunta'),
    (r'^enviar_ejercicio_corregir/$', 'k2Ejercicio.viewstab_alumno.enviar_ejercicio_corregir'),




 )