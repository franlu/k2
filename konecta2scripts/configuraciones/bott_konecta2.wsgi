import os, sys
sys.path.append('/home/brian')
sys.path.append('/home/brian/git/konecta2Django')
os.environ['DJANGO_SETTINGS_MODULE']='konecta2.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler())