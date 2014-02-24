#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('k2Usuario.views',
    (r'^logintab/$', 'login'),
    (r'^logoutab/$', 'logout'),
    (r'add/clase/$', 'setClase'),
 )