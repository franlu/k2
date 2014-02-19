from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'konecta2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('k2Ejercicio.urls')),
    url(r'^', include('k2Usuario.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
