from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
handler404 = 'konecta2app.views.file_not_found_404'
urlpatterns = patterns('',
    url(r'^$', 'konecta2app.views.index',name='index'),
    url(r'^', include('konecta2app.urls')),
    url(r'^', include('konecta2alumno.urls')),
    url(r'^', include('konecta2profesor.urls')),
    url(r'^', include('konecta2actualizar.urls')),
    url(r'^', include('konecta2correccion.urls')),             
    url(r'^admin/', include(admin.site.urls)),
)
