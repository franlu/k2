#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'^logintab/$', 'k2Usuario.views.login'),
    (r'^logoutab/$', 'k2Usuario.views.logout'),
    (r'^nueva/clase/$', 'k2Usuario.views.setClase'),
    (r'^ver/clases/$', 'k2Usuario.views.getClases')
 )