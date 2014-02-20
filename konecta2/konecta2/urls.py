# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from konecta2.settings import MEDIA_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'konecta2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('k2Ejercicio.urls')),
    url(r'^', include('k2Usuario.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )