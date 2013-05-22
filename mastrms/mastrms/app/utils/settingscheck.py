from django.conf import settings

def summary():
    for var in ['CHMOD_USER',
                'CHMOD_GROUP',
                'LOGS_TO_EMAIL',
                'KEYS_TO_EMAIL',
                'REGISTRATION_TO_EMAIL',
                'EMAIL_HOST',
                'SERVER_EMAIL',
                'RETURN_EMAIL',
                'MEMCACHE_SERVERS',
                'PERSISTENT_FILESTORE',
                'QUOTE_FILES_ROOT',
                'SITE_NAME',
                'EMAIL_APP_NAME',
                'DEBUG',
                'DEV_SERVER',
                'SSL_ENABLED',
                'SESSION_COOKIE_HTTPONLY',
                'SESSION_COOKIE_SECURE'

                ]:
        val = getattr(settings, var, 'Not Defined!')
        print '%s : %s' % (var, str(val))
