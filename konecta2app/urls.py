#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$','konecta2app.views.login'),
    url(r'^logout/$','konecta2app.views.logout'),
    url(r'^registro/$','konecta2app.views.registro'),
    url(r'^invitado/$','konecta2app.views.invitado'),
    url(r'^ver_usuarios/$','konecta2app.views.ver_usuarios'),
    url(r'^borrar_usuario/$','konecta2app.views.borrar_usuario'),
    url(r'^modificar_usuario/$','konecta2app.views.modificar_usuario'),
    url(r'^crear_notificacion/$','konecta2app.views.crear_notificacion'),
    url(r'^consultar_notificacion/$','konecta2app.views.consultar_notificacion'),
    url(r'^borrar_notificacion/$','konecta2app.views.borrar_notificacion'),
    url(r'^clases_profesor_usuarios/$','konecta2app.views.clases_profesor_usuarios'),
    url(r'^comprobar_pass/$','konecta2app.views.comprobar_pass'),
    url(r'^reiniciar_password/$','konecta2app.views.reiniciar_password'),
    url(r'^comprobar_token/$','konecta2app.views.comprobar_token'),
    url(r'^reset_password/$','konecta2app.views.reset_password'),


    #url(r'^insertar/$','konecta2app.insertarprofesores.insertar_profesores'),

)