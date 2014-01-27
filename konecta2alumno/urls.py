from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^todas_clases/$','konecta2alumno.views.todas_clases'),
    url(r'^ejercicios_pendientes/$','konecta2alumno.views.ejercicios_pendientes'),
    url(r'^detalles_ejercicio/$','konecta2alumno.views.detalles_ejercicio'),
)