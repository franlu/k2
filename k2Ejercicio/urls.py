#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'^cursos/$', 'k2Ejercicio.views.getCursos'),
    (r'^cursos/nuevo/$', 'k2Ejercicio.views.setCurso'),
    (r'^materias/$', 'k2Ejercicio.views.getMaterias'),
    (r'^materias/nueva/$', 'k2Ejercicio.views.setMateria'),
    (r'^temas/$', 'k2Ejercicio.views.getTemas'),
    (r'^temas/nuevo/$', 'k2Ejercicio.views.setTema'),
    (r'^ejercicios/$', 'k2Ejercicio.views.getEjercicios'),
    (r'^ejercicios/nuevo/$', 'k2Ejercicio.views.setEjercicio'),
    
 )