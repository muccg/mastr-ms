from settings import *
from os import environ

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

def get_env_setting(setting, default=None, islist=False):
    """
    Get the environment setting, return a default value, or raise
    an exception.
    Values used by this function will likely come from
    /etc/mastrms/mastrms.conf.
    """
    parse = lambda x: x.split() if islist else x
    try:
        return parse(environ["_".join([PROJECT_NAME, setting])])
    except KeyError:
        if default is None:
            from django.core.exceptions import ImproperlyConfigured
            error_msg = "Set the %s env variable" % setting
            raise ImproperlyConfigured(error_msg)
        else:
            return default

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

DEBUG = False

# Default SSL on and forced, turn off if necessary
SSL_ENABLED = True
SSL_FORCE = True

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

# see: https://docs.djangoproject.com/en/1.5/ref/settings/#admins
# see: https://docs.djangoproject.com/en/1.5/ref/settings/#managers
ADMINS = [
    ( 'alert', get_env_setting("alert_email", "root@localhost") )
]
MANAGERS = ADMINS

RETURN_EMAIL = get_env_setting("return_email", "Mastr-MS <noreply@yoursite.com>")

LOGS_TO_EMAIL = get_env_setting("logs_to_email", "log_email@yoursite.com")
KEYS_TO_EMAIL = get_env_setting("keys_to_email", "key_email@yoursite.com")
REGISTRATION_TO_EMAIL = get_env_setting("registration_to_email", "reg_email@yoursite.com")

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#server-email
SERVER_EMAIL = get_env_setting("server_email", "apache@localhost")

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#email-host
EMAIL_HOST = get_env_setting("email_host", "127.0.0.1")

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_env_setting("email_host_password", "")

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#email-host-user
EMAIL_HOST_USER = get_env_setting("email_host_user", "")

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#email-port
EMAIL_PORT = get_env_setting("email_port", 25)

# see: https://docs.djangoproject.com/en/1.5/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = "PROD: "

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#email-use-tls
EMAIL_USE_TLS = False

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = get_env_setting("allowed_hosts", [], True)

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

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

CHMOD_USER = get_env_setting("repo_user", "apache")
CHMOD_GROUP = get_env_setting("repo_group", "apache")

REPO_FILES_ROOT = get_env_setting("repo_files_root", os.path.join(CCG_WRITEABLE_DIRECTORY, 'files'))
QUOTE_FILES_ROOT = get_env_setting("quote_files_root", os.path.join(CCG_WRITEABLE_DIRECTORY, 'quotes'))

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

SECRET_KEY = get_env_setting("secret_key", "")

if get_env_setting("memcache", ""):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': get_env_setting("memcache", "", True),
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
