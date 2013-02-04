# -*- coding: utf-8 -*-
"""
Django settings import defaults for development server
"""
import os
from ccg.utils.webhelpers import url

# SCRIPT_NAME isnt set when not under wsgi
if not os.environ.has_key('SCRIPT_NAME'):
    os.environ['SCRIPT_NAME']=''

SCRIPT_NAME =   os.environ['SCRIPT_NAME']
#print 'Evaluating os.environ[PROJECT_DIRECTORY] as ', os.environ['PROJECT_DIRECTORY']
#PROJECT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

WEBAPP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIRECTORY = WEBAPP_ROOT

TMP_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'tmp')

#general site config
DEBUG = True
DEV_SERVER = True
SITE_ID = 1
APPEND_SLASH = True
SSL_ENABLED = False

# Locals ma
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

##
## Django Core stuff
##
TEMPLATE_LOADERS = [
#    'ccg.template.loaders.makoloader.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'userlog.middleware.RequestToThreadLocalMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'mastrms.app.utils.json_exception_handler_middleware.JSONExceptionHandlerMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'ccg.middleware.ssl.SSLRedirect',
    'django.contrib.messages.middleware.MessageMiddleware'
    #'ccg.middleware.StatsMiddleware.StatsMiddleware'
]

INSTALLED_APPS = [
    'mastrms.mdatasync_server',
    'mastrms.login',
    'mastrms.quote',
    'mastrms.admin',
    'mastrms.repository',
    'mastrms.users',
    'mastrms.app',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'userlog',
    'south'
]

AUTHENTICATION_BACKENDS = [
 'mastrms.repository.backend.MadasBackend',
 #'ccg.auth.backends.NoAuthModelBackend',
 'userlog.backend.AuthFailedLoggerBackend'
]

#email
EMAIL_HOST = 'example - smtp.yoursite.com'                      # Address of your smtp server
SERVER_EMAIL = "example - apache@yoursite.com"                  # from address for app emails to users
RETURN_EMAIL = "example - noreply@yoursite.com"                 # reply address for app emails to users
EMAIL_SUBJECT_PREFIX = "DEV "                           # email subject prefix
# default emails in case of server tracebacks, app failures, etc
ADMINS = [
    ( 'Tech Alerts', 'example - alerts@yoursite.com' )
]
MANAGERS = ADMINS

REGISTRATION_TO_EMAIL = 'example - someadmin@yoursite.com'        #An admin who will handle site registration emails

## Ldap
AUTH_LDAP_SERVER = '<your ldap server here>'
AUTH_LDAP_BASE = '<ldap base path>'
AUTH_LDAP_GROUP_BASE = '<ldap path to group base>'
AUTH_LDAP_ADMIN_BASE = '<ldap path to admin base>'
AUTH_LDAP_USER_BASE = 'ou=NEMA,ou=People,' + AUTH_LDAP_ADMIN_BASE

AUTH_LDAP_GROUPOC = 'groupofuniquenames'
AUTH_LDAP_USEROC = 'inetorgperson'
AUTH_LDAP_MEMBERATTR = 'uniqueMember'
AUTH_LDAP_USERDN = 'ou=People'


LDAPADMINUSERNAME = '<ldap admin path>'
LDAPADMINPASSWORD = '<your ldap server password here>'
AUTH_LDAP_GROUP = 'User'
DEFAULT_GROUP = 'madas'                 # Base group for users. Needs to exist in the database.
LDAP_DONT_REQUIRE_CERT = True           # dont require HTTPS for dev ldap

#Server side directories
PERSISTENT_FILESTORE = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '..', '..', 'files'))
#Ensure the persistent storage dir exits. If it doesn't, exit noisily.
assert (os.path.exists(PROJECT_DIRECTORY),
        "This application cannot start: Cannot find the project directory %s" % PROJECT_DIRECTORY)
assert (os.path.exists(PERSISTENT_FILESTORE),
        "This application cannot start: It expects a writeable directory at %s to use as a persistent filestore" % PERSISTENT_FILESTORE)

# for local development, this is set to the static serving directory. For deployment use Apache Alias
STATIC_SERVER_PATH = os.path.join(PROJECT_DIRECTORY, "app", "static")

# a directory that will be writable by the webserver, for storing various files...
WRITABLE_DIRECTORY = os.path.join(PROJECT_DIRECTORY,"scratch")
TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIRECTORY, "app", "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# mako compiled templates directory
MAKO_MODULE_DIR = os.path.join(WRITABLE_DIRECTORY, "app", "templates")
# mako module name
MAKO_MODULENAME_CALLABLE = ''

#MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY,"app", "static", "media")
#MEDIA_URL = url('/static1/')
ADMIN_MEDIA_PREFIX = url('/static/admin-media/')

TEMPLATE_DEBUG = DEBUG
LOGIN_URL = url('/accounts/login/')
LOGOUT_URL = url('/accounts/logout/')

STATIC_URL = url('/static/')
STATIC_ROOT = os.path.join(PROJECT_DIRECTORY, "static")

#session and cookies
MADAS_SESSION_TIMEOUT = 1800 #30 minute session timeout 
SESSION_COOKIE_PATH = url('/')
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_NAME = "csrftoken_madas_repoadmin"
SESSION_COOKIE_AGE = 60*60
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False

#functions to evaluate for status checking
# Hardcoded to list with one item of True for now, since that's what
# check_default() returns anyway and we have a namespace issue which is
# stopping import masterms.status_checks from working in this way.
#from mastrms.status_checks import *
#STATUS_CHECKS = [check_default]
STATUS_CHECKS = [True]

# memcache server list
MEMCACHE_SERVERS = ['yourmemcacheserver.yourdomain:11211','anothermemcacheserver.yourdomain:11211']
MEMCACHE_KEYSPACE = "mastrms-dev"


#APPLICATION SPECIFIC SETTINGS
ROOT_URLCONF = 'mastrms.urls'
SITE_NAME = 'madas'
SECRET_KEY = 'qj#tl@9@7((%^)$i#iyw0gcfzf&#a*pobgb8yr#1%65+*6!@g$'
EMAIL_APP_NAME = "MastrMS "
REPO_FILES_ROOT = PERSISTENT_FILESTORE
#quote files root should be within the repo files root
QUOTE_FILES_ROOT = os.path.join(REPO_FILES_ROOT, 'quotes')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mastrms',
        'USER': 'mastrms',
        'PASSWORD': 'mastrms',
        'HOST': '',                      
        'PORT': '',                      
    }
}

CHMOD_USER = 'apache'
CHMOD_GROUP = 'maupload'

#Datasync email settings:
LOGS_TO_EMAIL = "log_email@yoursite.com" #email address to receive datasync client log notifications
KEYS_TO_EMAIL = "key_email@yoursite.com" #email address to receive datasync key upload notifications


##
## LOGGING
##

LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "logs")
try:
    if not os.path.exists(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)
except:
    pass
os.path.exists(LOG_DIRECTORY), "No logs directory, please create one: %s" % LOG_DIRECTORY
INSTALL_NAME = PROJECT_DIRECTORY.split('/')[-2]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': 'MASTRMS [%(name)s:' + INSTALL_NAME + ':%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
        },
        'db': {
            'format': 'MASTRMS [%(name)s:' + INSTALL_NAME + ':%(duration)s:%(sql)s:%(params)s] %(message)s'
        },
        'simple': {
            'format': 'MASTRMS ' + INSTALL_NAME + ' %(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'errorfile':{
            'level':'ERROR',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'error.log'),
            'when':'midnight',
            'formatter': 'verbose'
        },
        'madasfile':{
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'mastrms.log'),
            'when':'midnight',
            'formatter': 'verbose'
        },
        'mdatasyncfile':{
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'mdatasync_server.log'),
            'when':'midnight',
            'formatter': 'verbose'
        },
        'db_logfile':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'mastrms_db.log'),
            'when':'midnight',
            'formatter': 'db'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'verbose',
            'include_html':True
        }
    },
    'root': {
            'handlers':['console', 'errorfile', 'mail_admins'],
            'level':'ERROR',
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': False,
            'level':'INFO',
        },
        'madas_log': {
            'handlers': ['madasfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'mdatasync_server_log': {
            'handlers': ['mdatasyncfile'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}