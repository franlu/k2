#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('k2Usuario.viewstab',
    (r'^logintab/$', 'login'),
    (r'^logoutab/$', 'logout'),
    (r'^clases_profesor/$', 'clases_profesor'),
    (r'^alumnos_por_clase/$', 'alumnos_por_clase'),
 )