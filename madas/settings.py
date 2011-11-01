# -*- coding: utf-8 -*-
# Django settings for project.
import os
from django.utils.webhelpers import url

# SCRIPT_NAME isnt set when not under wsgi
if not os.environ.has_key('SCRIPT_NAME'):
    os.environ['SCRIPT_NAME']=''

# PROJECT_DIRECTORY isnt set when not under wsgi
if not os.environ.has_key('PROJECT_DIRECTORY'):
    os.environ['PROJECT_DIRECTORY']=os.path.dirname(__file__).split("/appsettings/")[0]

SCRIPT_NAME =   os.environ['SCRIPT_NAME']
PROJECT_DIRECTORY = os.environ['PROJECT_DIRECTORY']


DEBUG = True
DEV_SERVER = True
SITE_ID = 1

# https
if SCRIPT_NAME:
    SSL_ENABLED = True
else:
    SSL_ENABLED = False

# Locale
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'logs')
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'madas.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'madas.mdatasync_server',
    #'madas.mdatasync_server.admin',
    'madas.dashboard',
    'madas.login',
    'madas.quote',
    'madas.users',
    'madas.admin',
    'madas.repository'
]

##
## Django Core stuff
##
TEMPLATE_LOADERS = [
    'django.template.loaders.makoloader.filesystem.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.email.EmailExceptionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.ssl.SSLRedirect'
]
TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIRECTORY,"templates","mako"), 
    os.path.join(PROJECT_DIRECTORY,"templates"),
]


MEMCACHE_KEYSPACE = "dev-madas-"

AUTHENTICATION_BACKENDS = [
 'madas.repository.backend.MadasBackend',
 #'django.contrib.auth.backends.LDAPBackend',
 'django.contrib.auth.backends.NoAuthModelBackend',
]

SESSION_COOKIE_PATH = url('/')
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_NAME = "csrftoken_madas_repoadmin"

PERSISTENT_FILESTORE = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '..', '..', 'files'))

if "LOCALDEV" in os.environ:
    SSL_ENABLED = False
    PERSISTENT_FILESTORE = os.path.normpath('/tmp/madas/filedata')

REPO_FILES_ROOT = PERSISTENT_FILESTORE
QUOTE_FILES_ROOT = os.path.join(PERSISTENT_FILESTORE, 'quotes')
MADAS_SESSION_TIMEOUT = 1800 #30 minute session timeout 

#Ensure the persistent storage dir exits. If it doesn't, exit noisily.
assert os.path.exists(PERSISTENT_FILESTORE), "This application cannot start: It expects a writeable directory at %s to use as a persistent filestore" % (PERSISTENT_FILESTORE) 

#functions to evaluate for status checking
from status_checks import *
STATUS_CHECKS = [check_default]

APPEND_SLASH = True
SITE_NAME = 'madas'

# these are non-standard and override defaults
MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY,"static")
MEDIA_URL = '/static/'


##
## LOGGING
##
import logging, logging.handlers
LOGGING_LEVEL = logging.DEBUG
install_name = PROJECT_DIRECTORY.split('/')[-2]
LOGGING_FORMATTER = logging.Formatter('[%(name)s:' + install_name + ':%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s')
LOGS = ['mdatasync_server_log', 'madas_log']
import ccglogging

#try an import of some local dev settings
try:
    from flat_settings_localdb import *
except ImportError, e:
    pass


# Override defaults with your local instance settings.
# They will be loaded from appsettings.ivecallocation, which can exist anywhere
# in the instance's pythonpath. This is a CCG convention designed to support
# global shared settings among multiple Django projects.
try:
    #not quite ready for this first one yet
    #from appsettings.mastrms import *
    from appsettings.default_dev import *
    from appsettings.mastrms.dev import *
except ImportError, e:
    print "Could not import appsettings.mastrms"

