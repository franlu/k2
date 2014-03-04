#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'^logintab/$', 'k2Usuario.views.login'),
    (r'^logoutab/$', 'k2Usuario.views.logout'),
    (r'^clases/nueva/$', 'k2Usuario.views.setClase'),
    (r'^clases/$', 'k2Usuario.views.getClases'),
    (r'^clases/alumnos/nuevo/$', 'k2Usuario.views.setAlumno'),
    (r'^clases/alumnos/$', 'k2Usuario.views.getAlumnos'),
    (r'^clases/alumnos/(?P<clase_id>\d+)/$', 'k2Usuario.views.getClaseAlumnos')
 )