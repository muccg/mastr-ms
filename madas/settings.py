# -*- coding: utf-8 -*-
"""
Django settings import defaults for development server
"""
import os
from django.utils.webhelpers import url

# SCRIPT_NAME isnt set when not under wsgi
if not os.environ.has_key('SCRIPT_NAME'):
    os.environ['SCRIPT_NAME']=''

SCRIPT_NAME =   os.environ['SCRIPT_NAME']
PROJECT_DIRECTORY = os.environ['PROJECT_DIRECTORY']

#general site config
DEBUG = True
DEV_SERVER = True
SITE_ID = 1
APPEND_SLASH = True

# https
if SCRIPT_NAME:
    SSL_ENABLED = True
else:
    SSL_ENABLED = False

# Locale
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

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

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
]

AUTHENTICATION_BACKENDS = [
 'madas.repository.backend.MadasBackend',
 #'django.contrib.auth.backends.LDAPBackend',
 'django.contrib.auth.backends.NoAuthModelBackend',
]

#email
EMAIL_HOST = 'ccg.murdoch.edu.au'
SERVER_EMAIL = "apache@ccg.murdoch.edu.au"                      # from address
RETURN_EMAIL = "apache@ccg.murdoch.edu.au"                      # from address
EMAIL_SUBJECT_PREFIX = "DEV "
RETURN_EMAIL = 'bpower@ccg.murdoch.edu.au'
# default emails
ADMINS = [
    ( 'Tech Alerts', 'alerts@ccg.murdoch.edu.au' )
]
MANAGERS = ADMINS

## Ldap
AUTH_LDAP_SERVER = 'ldaps://fdsdev.localdomain'
DEFAULT_GROUP = 'madas'  #this needs to exist in the database.
AUTH_LDAP_BASE = 'ou=People,dc=ccg,dc=murdoch,dc=edu,dc=au'
AUTH_LDAP_GROUP_BASE = 'ou=NEMA,ou=Web Groups,dc=ccg,dc=murdoch,dc=edu,dc=au'
AUTH_LDAP_ADMIN_BASE = 'dc=ccg,dc=murdoch,dc=edu,dc=au'
AUTH_LDAP_USER_BASE = 'ou=NEMA,ou=People,' + AUTH_LDAP_ADMIN_BASE
LDAPADMINUSERNAME = 'uid=nemaapp,ou=Application Accounts'
LDAPADMINPASSWORD = 'nr2WovGfkWR'
AUTH_LDAP_GROUP = 'User'
# dont require HTTPS for dev ldap
LDAP_DONT_REQUIRE_CERT = True

#Server side directories
PERSISTENT_FILESTORE = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '..', '..', 'files'))
if "LOCALDEV" in os.environ:
    SSL_ENABLED = False
    PERSISTENT_FILESTORE = os.path.normpath('/tmp/madas/filedata')
#Ensure the persistent storage dir exits. If it doesn't, exit noisily.
assert os.path.exists(PERSISTENT_FILESTORE), "This application cannot start: It expects a writeable directory at %s to use as a persistent filestore" % (PERSISTENT_FILESTORE) 
# for local development, this is set to the static serving directory. For deployment use Apache Alias
STATIC_SERVER_PATH = os.path.join(PROJECT_DIRECTORY,"static")
# a directory that will be writable by the webserver, for storing various files...
WRITABLE_DIRECTORY = os.path.join(PROJECT_DIRECTORY,"scratch")
TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIRECTORY,"templates","mako"), 
    os.path.join(PROJECT_DIRECTORY,"templates"),
]
# mako compiled templates directory
MAKO_MODULE_DIR = os.path.join(WRITABLE_DIRECTORY, "templates")
# mako module name
MAKO_MODULENAME_CALLABLE = ''

MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY,"static")
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = url('/static/admin-media/')

LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'logs')
TEMPLATE_DEBUG = DEBUG
LOGIN_URL = url('/accounts/login/')
LOGOUT_URL = url('/accounts/logout/')


#session and cookies
MADAS_SESSION_TIMEOUT = 1800 #30 minute session timeout 
SESSION_COOKIE_PATH = url('/')
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_NAME = "csrftoken_madas_repoadmin"
SESSION_COOKIE_AGE = 60*60

#functions to evaluate for status checking
from status_checks import *
STATUS_CHECKS = [check_default]

# memcache server list
MEMCACHE_SERVERS = ['memcache1.localdomain:11211','memcache2.localdomain:11211']
MEMCACHE_KEYSPACE = "mastrms-dev"


#APPLICATION SPECIFIC SETTINGS
ROOT_URLCONF = 'madas.urls'
SITE_NAME = 'madas'
SECRET_KEY = 'qj#tl@9@7((%^)$i#iyw0gcfzf&#a*pobgb8yr#1%65+*6!@g$'
EMAIL_APP_NAME = "MastrMS "
REPO_FILES_ROOT = PERSISTENT_FILESTORE
QUOTE_FILES_ROOT = os.path.join(PERSISTENT_FILESTORE, 'quotes')

INSTALLED_APPS.extend([
    'madas.mdatasync_server',
    'madas.dashboard',
    'madas.login',
    'madas.quote',
    'madas.users',
    'madas.admin',
    'madas.repository'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<your database name here>',
        'USER': '<your database user here>',
        'PASSWORD': '<your database user password here>',
        'HOST': '<your database host here>',                      
        'PORT': '',                      
    }
}

CHMOD_USER = 'apache'
CHMOD_GROUP = 'maupload'

#Datasync email settings:
LOGS_TO_EMAIL = "<email address to receive datasync client log notifications>"
KEYS_TO_EMAIL = "<email address to receive datasync key upload notifications>"


##
## LOGGING
##
import logging, logging.handlers
LOGGING_LEVEL = logging.DEBUG
install_name = PROJECT_DIRECTORY.split('/')[-2]
LOGGING_FORMATTER = logging.Formatter('[%(name)s:' + install_name + ':%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s')
LOGS = ['mdatasync_server_log', 'madas_log']
import ccglogging

# Override defaults with your local instance settings.
# They will be loaded from appsettings.<projectname>, which can exist anywhere
# in the instance's pythonpath. This is a CCG convention designed to support
# global shared settings among multiple Django projects.
try:
    from appsettings.mastrms import *
except ImportError, e:
    pass

#If you have a local settings file which overrides these, try importing it here
try:
    from settings_local import *
except ImportError, e:
    pass

