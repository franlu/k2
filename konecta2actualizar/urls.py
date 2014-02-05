#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^servidor/actualizar/$','konecta2actualizar.views.actualizar_k2'),
)