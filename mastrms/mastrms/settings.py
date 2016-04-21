# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers
from ccg_django_utils.conf import EnvConfig

env = EnvConfig()

CCG_INSTALL_ROOT = os.path.dirname(os.path.realpath(__file__))
CCG_WRITEABLE_DIRECTORY = os.path.join(CCG_INSTALL_ROOT,"scratch")
PROJECT_NAME = os.path.basename(CCG_INSTALL_ROOT)

# see ccg_django_utils.webhelpers
BASE_URL_PATH = os.environ.get("SCRIPT_NAME", "")

# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = env.getlist("allowed_hosts", ["*"])

DATABASES = {
    'default': {
        'ENGINE': env.get_db_engine("dbtype", "pgsql"),
        'NAME': env.get("dbname", "mastrms"),
        'USER': env.get("dbuser", "mastrms"),
        'PASSWORD': env.get("dbpass", "mastrms"),
        'HOST': env.get("dbserver", ""),
        'PORT': env.get("dbport", ""),
    }
}

# see: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = [
    'userlog.middleware.RequestToThreadLocalMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'ccg_django_utils.middleware.ssl.SSLRedirect',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# see: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = [
    'mastrms.users',
    'mastrms.mdatasync_server',
    'mastrms.login',
    'mastrms.quote',
    'mastrms.admin',
    'mastrms.repository',
    'mastrms.app',
    'mastrms.api',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_extensions',
    'userlog',
    'south',
    'django_nose',
    'rest_framework',
    'rest_framework.authtoken',
]

# these determine which authentication method to use
# apps use modelbackend by default, but can be overridden here
# see: https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'userlog.backend.AuthFailedLoggerBackend',
]

# New feature in Django 1.5 -- custom user models
AUTH_USER_MODEL = 'users.User'

# Make this unique, and don't share it with anybody.
# see: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env.get("secret_key", "" if env.get("production", False) else "change-it")

# Default SSL on and forced, turn off if necessary
SSL_ENABLED = env.get("production", False)
SSL_FORCE = env.get("production", False)

# Debug off by default
DEBUG = not env.get("production", False)

# Default the site ID to 1, even if the sites framework isn't being used
SITE_ID = 1
SITE_URL = env.get("self_url_path", "")

# see: https://docs.djangoproject.com/en/1.4/ref/settings/#root-urlconf
ROOT_URLCONF = 'mastrms.urls'

# This one's a constant, where puppet will have collect static files to
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#static-root
STATIC_ROOT=os.path.join(CCG_INSTALL_ROOT, 'static')

# These may be overridden, but it would be nice to stick to this convention
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#static-url
STATIC_URL = '{0}/static/'.format(BASE_URL_PATH)

# Another puppet-enforced content for location of user-uploaded data
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#media-root
MEDIA_ROOT = os.path.join(CCG_WRITEABLE_DIRECTORY,"static","media")

# This may be overridden
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#media-url
MEDIA_URL = '{0}/static/media/'.format(BASE_URL_PATH)

# All templates must be loaded from within an app, so these are the only
# ones that should be enabled.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#template-loaders
TEMPLATE_LOADERS = [
    'django.template.loaders.app_directories.Loader'
]

# Default all email to ADMINS and MANAGERS to root@localhost.
# Puppet redirects this to something appropriate depend on the environment.
# see: https://docs.djangoproject.com/en/1.6/ref/settings/#admins
# see: https://docs.djangoproject.com/en/1.6/ref/settings/#managers
ADMINS = [
    ( 'alert', env.get("alert_email", "root@localhost") )
]
MANAGERS = ADMINS

# email settings
# See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-host
EMAIL_HOST = env.get("email_host", "")
# See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-port
EMAIL_PORT = env.get("email_port", 25)

# See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-host-user
EMAIL_HOST_USER = env.get("email_host_user", "")
# See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = env.get("email_host_password", "")

# See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-use-tls
EMAIL_USE_TLS = env.get("email_use_tls", False)

# see: https://docs.djangoproject.com/en/1.6/ref/settings/#email-subject-prefix
EMAIL_APP_NAME = "Mastr-MS "
EMAIL_SUBJECT_PREFIX = env.get("email_subject_prefix", "PROD: " if env.get("production", False) else "DEV ")

# See: https://docs.djangoproject.com/en/1.6/ref/settings/#email-backend
if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
elif DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(CCG_WRITEABLE_DIRECTORY, "mail")
    if not os.path.exists(EMAIL_FILE_PATH):
        os.mkdir(EMAIL_FILE_PATH)

# See: https://docs.djangoproject.com/en/1.6/ref/settings/#server-email
SERVER_EMAIL = env.get("server_email", "noreply@mastrms")

RETURN_EMAIL = env.get("return_email", "Mastr-MS <noreply@yoursite.com>")

# email address to receive datasync client log notifications
LOGS_TO_EMAIL = env.get("logs_to_email", "log_email@yoursite.com")
# email address to receive datasync key upload notifications
KEYS_TO_EMAIL = env.get("keys_to_email", "key_email@yoursite.com")
# email address to receive registration requests
REGISTRATION_TO_EMAIL = env.get("registration_to_email", "reg_email@yoursite.com")

# Default cookie settings
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#session-cookie-age and following
SESSION_COOKIE_AGE = 60*60
SESSION_COOKIE_PATH = '{0}/'.format(BASE_URL_PATH)
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # Use Django's standard `django.contrib.auth` permissions.
        'rest_framework.permissions.DjangoModelPermissions',
    ],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

# This honours the X-Forwarded-Host header set by our nginx frontend when
# constructing redirect URLS.
# see: https://docs.djangoproject.com/en/1.4/ref/settings/#use-x-forwarded-host
USE_X_FORWARDED_HOST = True

# Log directory created and enforced by puppet
CCG_LOG_DIRECTORY = os.path.join(CCG_INSTALL_ROOT, "log")

# Default logging configuration, can be overridden
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(name)s:%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
        },
        'db': {
            'format': '[%(name)s:%(duration)s:%(sql)s:%(params)s] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(filename)s:%(lineno)s (%(funcName)s)  %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, 'mastrms.log'),
            'when': 'midnight',
            'formatter': 'verbose'
        },
        'db_logfile':{
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(CCG_LOG_DIRECTORY, 'mastrms_db.log'),
            'when': 'midnight',
            'formatter': 'db'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html':True
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file', ],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['db_logfile', 'mail_admins'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'mastrms': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

if env.get("memcache", False):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': env.getlist("memcache", []),
            'KEYSPACE': "%s-prod" % PROJECT_NAME,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
NOSE_PLUGINS = ["mastrms.testutils.noseplugins.SilenceSouthPlugin"]

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

CHMOD_USER = env.get("repo_user", "apache")
CHMOD_GROUP = env.get("repo_group", "apache")

REPO_FILES_ROOT = env.get("repo_files_root", os.path.join(CCG_WRITEABLE_DIRECTORY, 'files'))
QUOTE_FILES_ROOT = env.get("quote_files_root", os.path.join(CCG_WRITEABLE_DIRECTORY, 'quotes'))

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
