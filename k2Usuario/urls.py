#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from k2Usuario.views import ClaseList

urlpatterns = patterns('',
    (r'^clases/nueva/$', 'k2Usuario.views.setClase'),
    (r'^clases/$', 'k2Usuario.views.getClases'),
    url (r'^clases/$', login_required(ClaseList.as_view()), name='claselist'),
    (r'^clases/alumnos/nuevo/$', 'k2Usuario.views.setAlumno'),
    (r'^clases/alumnos/$', 'k2Usuario.views.getAlumnos'),
    (r'^clases/alumnos/(?P<clase_id>\d+)/$', 'k2Usuario.views.getAlumnosClase')
 )