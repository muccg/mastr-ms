from settings import *
from os import environ

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

def get_env_setting(setting, default=None):
    """ Get the environment setting or return exception """
    try:
        return environ["_".join([PROJECT_NAME, setting])]
    except KeyError:
        if default is None:
            from django.core.exceptions import ImproperlyConfigured
            error_msg = "Set the %s env variable" % setting
            raise ImproperlyConfigured(error_msg)
        else:
            return default

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

DEBUG = False

# extra email settings
# see: https://docs.djangoproject.com/en/1.5/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = "PROD: "

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

ALLOWED_HOSTS = get_env_setting("allowed_hosts", [])

engines = {
    'pgsql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
    'sqlite3': 'django.db.backends.sqlite3',
}

DATABASES = {
    'default': {
        'ENGINE': engines.get(get_env_setting("dbtype", ""), engines["pgsql"]),
        'NAME': get_env_setting("dbname", "mastrms"),
        'USER': get_env_setting("dbuser", "mastrms"),
        'PASSWORD': get_env_setting("dbpass", ""),
        'HOST': get_env_setting("dbserver", ""),
        'PORT': get_env_setting("dbport", ""),
    }
}

SECRET_KEY = get_env_setting("secret_key", "")

if get_env_setting("memcache", ""):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': get_env_setting("memcache"),
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

try:
    from localsettings import *
except ImportError, e:
    pass
