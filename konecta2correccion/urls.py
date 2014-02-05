#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^guardar_nota/$','konecta2correccion.views.guardar_nota'),
    url(r'^ver_notas/$','konecta2correccion.views.ver_notas'),
    url(r'^ver_notas_detallado/$','konecta2correccion.views.ver_notas_detallado'),
    url(r'^estado_ejercicios/$','konecta2correccion.views.estado_ejercicios'),
    url(r'^guardar_nota_array/$','konecta2correccion.views.guardar_nota_array'),
)