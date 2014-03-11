#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',


    (r'^clases/nueva/$', 'k2Usuario.views.setClase'),
    (r'^clases/$', 'k2Usuario.views.getClases'),
    (r'^clases/alumnos/nuevo/$', 'k2Usuario.views.setAlumno'),
    (r'^clases/alumnos/$', 'k2Usuario.views.getAlumnos'),
    (r'^clases/alumnos/(?P<clase_id>\d+)/$', 'k2Usuario.views.getAlumnosClase')
 )