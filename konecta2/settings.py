# -*- coding: utf-8 -*-

"""
Django settings for konecta2 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname("__file__")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64n8mi+=gsy3fwq(%gbe9rxd#_25=s*-%$-((ue5&z8dnyjgs2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'suit', #If you deploy your project with Apache or Debug=False dont forget to run ./manage.py collectstatic
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'floppyforms',
    'bootstrapform',
    'dajaxice',
    'dajax',
    'konecta2',
    'k2Ejercicio',
    'k2Usuario',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'k2templates')]

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'konecta2.processors.comun',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

ROOT_URLCONF = 'konecta2.urls'

WSGI_APPLICATION = 'konecta2.wsgi.application'

LANGUAGE_CODE = 'es-es'

SESSION_COOKIE_AGE = 18000 #seg
SESSION_SAVE_EVERY_REQUEST = True

SITE_ID = 1
COLLEGE_ID = '0000'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'k2media')
MEDIA_URL = '/media/'
MEDIA_VIDEO = MEDIA_ROOT + '/video/'
MEDIA_AUDIO = MEDIA_ROOT + '/audio/'
MEDIA_IMAGE = MEDIA_ROOT + '/image/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/pizarra/'

# Add to your settings file
CONTENT_TYPES = ['image', 'video', 'audio']
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "5242880"

try:
  import local_settings
except ImportError:
  print """
    -------------------------------------------------------------------------
    You need to create a local_settings.py file which needs to contain at least
    database connection information.
    -------------------------------------------------------------------------
    """
  import sys
  sys.exit(1)
else:
  # Import any symbols that begin with A-Z. Append to lists any symbols that
  # begin with "EXTRA_".
  import re
  for attr in dir(local_settings):
    match = re.search('^EXTRA_(\w+)', attr)
    if match:
      name = match.group(1)
      value = getattr(local_settings, attr)
      try:
        globals()[name] += value
      except KeyError:
        globals()[name] = value
    elif re.search('^[A-Z]', attr):
      globals()[attr] = getattr(local_settings, attr)