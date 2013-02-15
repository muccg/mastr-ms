# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers

CCG_INSTALL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CCG_WRITEABLE_DIRECTORY = os.path.join(CCG_INSTALL_ROOT,"writeable")

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

# see: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # !!! Disabled in original code !!!
    #'django.middleware.csrf.CsrfViewMiddleware',
    'ccg.middleware.ssl.SSLRedirect',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# see: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
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

# these determine which authentication method to use
# apps use modelbackend by default, but can be overridden here
# see: https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend'
]

# We have a puppet function to generate these by hashing appname and a secret
SECRET_KEY = 'change-it'

# Default SSL on and forced, turn off if necessary
SSL_ENABLED = False # Changed from True
SSL_FORCE = False # Changed from True

# Debug off by default
DEBUG = True # Changed from False

# Default the site ID to 1, even if the sites framework isn't being used
SITE_ID = 1

# see: https://docs.djangoproject.com/en/1.4/ref/settings/#root-urlconf
ROOT_URLCONF = 'mastrms.urls'

# This one's a constant, where puppet will have collect static files to
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#static-root
STATIC_ROOT=os.path.join(CCG_INSTALL_ROOT, 'static')

# These may be overridden, but it would be nice to stick to this convention
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#static-url
STATIC_URL = '{0}/static/'.format(os.environ.get("SCRIPT_NAME", ""))

# Another puppet-enforced content for location of user-uploaded data
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#media-root
MEDIA_ROOT = os.path.join(CCG_WRITEABLE_DIRECTORY,"static","media")

# This may be overridden
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#media-url
MEDIA_URL = '{0}/static/media/'.format(os.environ.get("SCRIPT_NAME", ""))

# All templates must be loaded from within an app, so these are the only
# ones that should be enabled.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#template-loaders
TEMPLATE_LOADERS = [
    'django.template.loaders.app_directories.Loader'
]

# Default all email to ADMINS and MANAGERS to root@localhost.
# Puppet redirects this to something appropriate depend on the environment.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#admins
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#managers
ADMINS = [
    ( 'alert', 'root@localhost' )
]
MANAGERS = ADMINS

# Mail relay settings for those projects that need it
# Local non-smtp delivery and forwarding is the alternative
EMAIL_USE_TLS = False
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 25
EMAIL_APP_NAME = "mastrms"
SERVER_EMAIL = "apache@localhost"  # from address

# Default cookie settings
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#session-cookie-age and following
SESSION_COOKIE_AGE = 60*60
SESSION_COOKIE_PATH = '{0}/'.format(os.environ.get("SCRIPT_NAME", ""))
SESSION_COOKIE_NAME = 'mastrms_sessionid'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = False # CHange from True
SESSION_COOKIE_SECURE = False # Changed from True

# see: https://docs.djangoproject.com/en/1.4/ref/settings/#csrf-cookie-name and following
CSRF_COOKIE_NAME = "csrftoken_mastrms"
CSRF_COOKIE_SECURE = False # Changed from True

# Default date input formats, may be overridden
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#date-input-formats
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-us'
USE_I18N = False
USE_L10N = False
DATE_INPUT_FORMATS = ('%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y','%d %m %Y','%d %m %y', '%d %b %Y')
DATE_FORMAT = "d-m-Y"
SHORT_DATE_FORMAT = "d/m/Y"

# This honours the X-Forwarded-Host header set by our nginx frontend when
# constructing redirect URLS.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#use-x-forwarded-host
USE_X_FORWARDED_HOST = True

# Log directory created and enforced by puppet
CCG_LOG_DIRECTORY = os.path.join(CCG_WRITEABLE_DIRECTORY, "logs")

# Default logging configuration, can be overridden
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': 'mastrms [%(name)s:%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
        },
        'db': {
            'format': 'mastrms [%(name)s:%(duration)s:%(sql)s:%(params)s] %(message)s'
        },
        'simple': {
            'format': 'mastrms %(levelname)s %(message)s'
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
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, 'mastrms.log'),
            'when':'midnight',
            'formatter': 'verbose'
        },
        'db_logfile':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, 'mastrms_db.log'),
            'when':'midnight',
            'formatter': 'db'
        },
        'syslog':{
            'level':'DEBUG',
            'class':'logging.handlers.SysLogHandler',
            'address':'/dev/log',
            'facility':'local4',
            'formatter': 'verbose'
        },        
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'verbose',
            'include_html':True
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['file', 'syslog', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['db_logfile', 'mail_admins'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'mastrms': {
            'handlers': ['console', 'file', 'syslog'],
            'level': 'DEBUG'
        }
    }
}

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

CHMOD_USER = 'apache'
CHMOD_GROUP = 'maupload'

REPO_FILES_ROOT = os.path.join(CCG_WRITEABLE_DIRECTORY, 'files')
QUOTE_FILES_ROOT = os.path.join(CCG_WRITEABLE_DIRECTORY, 'quotes')

RETURN_EMAIL = "example - noreply@yoursite.com"

LOGS_TO_EMAIL = "log_email@yoursite.com" #email address to receive datasync client log notifications
KEYS_TO_EMAIL = "key_email@yoursite.com" #email address to receive datasync key upload notifications

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

try:
    print "Attempting to import local settings as appsettings.mastrms"
    from appsettings.mastrms import *
    print "Successfully imported appsettings.mastrms"
except ImportError, e:
    print "Failed to import appsettings.mastrms"