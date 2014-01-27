import os, sys
sys.path.append('/home/konecta2')
sys.path.append('/home/konecta2/git/konecta2Django')
os.environ['DJANGO_SETTINGS_MODULE']='konecta2.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()