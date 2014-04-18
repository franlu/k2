#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from k2Ejercicio.views import CursoList, CursoCreate, CursoUpdate, CursoDelete
from k2Ejercicio.views import MateriaList, MateriaCreate, MateriaUpdate, MateriaDelete
from k2Ejercicio.views import TemaList, TemaCreate, TemaUpdate, TemaDelete
from k2Ejercicio.views import EjercicioList, EjercicioCreate, EjercicioUpdate, EjercicioDelete, EjercicioDetailView
from k2Ejercicio.views import videocreate, videodelete, imagecreate, imagedelete, textocreate, textodelete
from k2Ejercicio.views import escrituralibrecreate, escrituralibredelete

urlpatterns = patterns('',
    #curso
    url(r'^cursos/$', login_required(CursoList.as_view()) , name='cursolist'),
    url(r'^cursos/nuevo/$', login_required(CursoCreate.as_view()) , name='cursocreate'),
    url(r'^cursos/editar/(?P<pk>\d+)$', login_required(CursoUpdate.as_view()) , name='cursoupdate'),
    url(r'^cursos/borrar/(?P<pk>\d+)$', login_required(CursoDelete.as_view()) , name='cursodelete'),

    #materia
    url(r'^materias/$', login_required(MateriaList.as_view()) , name='materialist'),
    url(r'^materias/nueva/$', login_required(MateriaCreate.as_view()) , name='materiacreate'),
    url(r'^materias/editar/(?P<pk>\d+)$', login_required(MateriaUpdate.as_view()) , name='materiaupdate'),
    url(r'^materias/borrar/(?P<pk>\d+)$', login_required(MateriaDelete.as_view()) , name='materiadelete'),

    #tema
    url(r'^temas/$', login_required(TemaList.as_view()) , name='temalist'),
    url(r'^temas/nuevo/$', login_required(TemaCreate.as_view()) , name='temacreate'),
    url(r'^temas/editar/(?P<pk>\d+)$', login_required(TemaUpdate.as_view()) , name='temaupdate'),
    url(r'^temas/borrar/(?P<pk>\d+)$', login_required(TemaDelete.as_view()) , name='temadelete'),

    #ejercicio
    url(r'^ejercicios/$', login_required(EjercicioList.as_view()) , name='ejerciciolist'),
    url(r'^ejercicios/nuevo/$', login_required(EjercicioCreate.as_view()) , name='ejerciciocreate'),
    url(r'^ejercicios/editar/(?P<pk>\d+)$', login_required(EjercicioUpdate.as_view()) , name='ejercicioupdate'),
    url(r'^ejercicios/borrar/(?P<pk>\d+)$', login_required(EjercicioDelete.as_view()) , name='ejerciciodelete'),
    url(r'^ejercicios/ref/(?P<pk>\d+)/$', login_required(EjercicioDetailView.as_view()) , name='ejerciciodetail'),


     url(r'^ejercicios/(?P<pk>\d+)/video/nuevo/$', login_required(videocreate.as_view()), name='videocreate'),
     url(r'^ejercicios/(?P<pk>\d+)/video/borrar/(?P<pk1>\d+)/$', videodelete, name='videodelete'),
     url(r'^ejercicios/(?P<pk>\d+)/image/nuevo/$', login_required(imagecreate.as_view()), name='imagecreate'),
     url(r'^ejercicios/(?P<pk>\d+)/image/borrar/(?P<pk1>\d+)/$', imagedelete, name='imagedelete'),
     url(r'^ejercicios/(?P<pk>\d+)/texto/nuevo/$', login_required(textocreate.as_view()), name='textocreate'),
     url(r'^ejercicios/(?P<pk>\d+)/texto/borrar/(?P<pk1>\d+)/$', textodelete, name='textodelete'),
     url(r'^ejercicios/(?P<pk>\d+)/escrituralibre/nuevo/$', login_required(escrituralibrecreate.as_view()), name='escrituralibrecreate'),
     url(r'^ejercicios/(?P<pk>\d+)/escrituralibre/borrar/(?P<pk1>\d+)/$', escrituralibredelete, name='escrituralibredelete'),


 )