# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from konecta2.settings import MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'konecta2.views.inicio', name='inicio'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logout.html'}),
    url(r'^pizarra/$', 'konecta2.views.pizarra', name='pizarra'),
    url(r'^pizarra/', include('k2Ejercicio.urls')),
    url(r'^pizarra/', include('k2Usuario.urls')),

    #Direcciones para las tablets
    url(r'^', include('k2Usuario.urlstab')),
    url(r'^', include('k2Ejercicio.urlstab')),

    url(r'^admin/', include(admin.site.urls)),

    #dajaxice
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

    # Media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )