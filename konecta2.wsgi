import os, sys

sys.path.append('/home/brian/git/konecta2django/')
os.environ['DJANGO_SETTINGS_MODULE']='konecta2.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()