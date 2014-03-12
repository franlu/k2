#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from k2Usuario.views import AlumnoList, AlumnosClaseList, ClaseList, ClaseCreate, ClaseUpdate, ClaseDelete

urlpatterns = patterns('',
    url(r'^clases/crear/$', login_required(ClaseCreate.as_view()), name='clasecreate'),
    url(r'^clases/editar/(?P<pk>\d+)$', login_required(ClaseUpdate.as_view()), name='claseupdate'),
    url(r'^clases/borrar/(?P<pk>\d+)$', login_required(ClaseDelete.as_view()), name='clasedelete'),
    url (r'^clases/$', login_required(ClaseList.as_view()), name='claselist'),
    (r'^clases/alumnos/nuevo/$', 'k2Usuario.views.setAlumno'),
    url(r'^clases/alumnos/$', login_required(AlumnoList.as_view()), name='alumnolist'),
    url(r'^clases/alumnos/(?P<clase_id>\d+)/$', login_required(AlumnosClaseList.as_view()), name='alumnosclaselist')
 )