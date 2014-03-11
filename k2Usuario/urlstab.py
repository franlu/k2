#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'^logintab/$', 'k2Usuario.viewstab.login'),
    (r'^logoutab/$', 'k2Usuario.viewstab.logout'),
    (r'^clases_profesor/$', 'k2Usuario.viewstab.clases_profesor'),
    (r'^alumnos_por_clase/$', 'k2Usuario.viewstab.alumnos_por_clase'),



 )