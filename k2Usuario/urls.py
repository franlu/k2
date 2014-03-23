#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from k2Usuario.views import AlumnoCreate, AlumnoUpdate, AlumnoDelete, AlumnoList, ClaseAlumnosList, ClaseList, ClaseCreate, ClaseUpdate, ClaseDelete

urlpatterns = patterns('',
    #Clase
    url (r'^clases/$', login_required(ClaseList.as_view()), name='claselist'),
    url(r'^clases/crear/$', login_required(ClaseCreate.as_view()), name='clasecreate'),
    url(r'^clases/editar/(?P<pk>\d+)$', login_required(ClaseUpdate.as_view()), name='claseupdate'),
    url(r'^clases/borrar/(?P<pk>\d+)$', login_required(ClaseDelete.as_view()), name='clasedelete'),
    url(r'^clases/alumnos/(?P<clase_id>\d+)/$', login_required(ClaseAlumnosList.as_view()), name='clasealumnoslist'),

    #Alumno
    url(r'^alumnos/$', login_required(AlumnoList.as_view()), name='alumnolist'),
    url(r'^alumnos/crear/$', login_required(AlumnoCreate.as_view()), name='alumnocreate'),
    url(r'^alumnos/editar/(?P<pk>\d+)$', login_required(AlumnoUpdate.as_view()), name='alumnoupdate'),
    url(r'^alumnos/borrar/(?P<pk>\d+)$', login_required(AlumnoDelete.as_view()), name='alumnodelete'),

 )