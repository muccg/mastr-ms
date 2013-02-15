import os
from django.conf import settings

DEBUG = True

SSL_ENABLED = False
SSL_FORCE = False

SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SECURE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mastrms',
        'USER': 'mastrmsapp',
        'PASSWORD': 'mastrmsapp',
        'HOST': '',                      
        'PORT': '',                      
    }
}

# MASTRMS apps to be added to INSTALLED_APPS
APPS = [
    'mastrms.mdatasync_server', 
    'mastrms.login', 
    'mastrms.quote', 
    'mastrms.admin', 
    'mastrms.users', 
    'mastrms.app', 
    'mastrms.repository'
]

settings.INSTALLED_APPS = APPS + settings.INSTALLED_APPS

#MASTRMS apps to be appended to INSTALLED_APPS
settings.INSTALLED_APPS.append('userlog')
settings.INSTALLED_APPS.append('south')

#Not used for this project at the moment
settings.MIDDLEWARE_CLASSES.remove('django.middleware.csrf.CsrfViewMiddleware')

CHMOD_USER = 'apache'
CHMOD_GROUP = 'maupload'

REPO_FILES_ROOT = os.path.join(settings.CCG_WRITEABLE_DIRECTORY, 'files')
QUOTE_FILES_ROOT = os.path.join(settings.CCG_WRITEABLE_DIRECTORY, 'quotes')

RETURN_EMAIL = "example - noreply@yoursite.com"

LOGS_TO_EMAIL = "log_email@yoursite.com" #email address to receive datasync client log notifications
KEYS_TO_EMAIL = "key_email@yoursite.com" #email address to receive datasync key upload notifications