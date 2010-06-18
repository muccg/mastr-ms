# -*- coding: utf-8 -*-
# Django settings for project.
import os
from django.utils.webhelpers import url

from build.settings.defaults.prod import *
from build.settings.db.prod import *
from build.settings.ldap.prod import *

ADMINS.append( ( 'Andrew Macgregor', 'andrew@ccg.murdoch.edu.au' ) )

DATABASES['default']['NAME'] = 'dev_madas'
DATABASES['default']['USER'] = 'madasapp'
DATABASES['default']['PASSWORD'] = 'madasapp'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'qj#tl@9@7((%^)$i#iyw0gcfzf&#a*pobgb8yr#1%65+*6!@g$'

ROOT_URLCONF = 'madas.urls'

INSTALLED_APPS.extend( [
    'madas.mdatasync_server',
    'madas.m',
    'madas.dashboard',
    'madas.login',
    'madas.quote',
    'madas.users',
    'madas.admin',
    'madas.repository'
] )

MEMCACHE_KEYSPACE = "dev-madas-"

# override the LDAP group
DEFAULT_GROUP = 'madas'  #this needs to exist in the database.
AUTH_LDAP_BASE = 'ou=People,dc=ccg,dc=murdoch,dc=edu,dc=au'
AUTH_LDAP_GROUP_BASE = 'ou=NEMA,ou=Web Groups,dc=ccg,dc=murdoch,dc=edu,dc=au'
AUTH_LDAP_ADMIN_BASE = 'dc=ccg,dc=murdoch,dc=edu,dc=au'
AUTH_LDAP_USER_BASE = 'ou=NEMA,ou=People,' + AUTH_LDAP_ADMIN_BASE
LDAPADMINUSERNAME = 'uid=nemaapp,ou=Application Accounts'
LDAPADMINPASSWORD = 'nr2WovGfkWR'
MADAS_STATUS_GROUPS = ['User', 'Pending', 'Deleted', 'Rejected']
MADAS_ADMIN_GROUPS = ['Administrators', 'Node Reps']

AUTHENTICATION_BACKENDS = [
 'madas.repository.backend.MadasBackend',
 #'django.contrib.auth.backends.LDAPBackend',
 'django.contrib.auth.backends.NoAuthModelBackend',
]

SESSION_COOKIE_PATH = url('/')
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_NAME = "csrftoken_madas_repoadmin"

# a directory for persistent storage on the filesystem for this app. 
# it is 'DECLARED' here for readability, set below based on whether 
# the site is being run locally, on a dev server, or on a production server,
# and then asserted towards the end of this file. 
# It should be created outside of PROJECT_DIR, and the application should fail 
# on startup if it does not exist (hence the assert)
PERSISTENT_FILESTORE = None
PERSISTENT_FILESTORE = os.path.normpath(os.path.join(PROJECT_DIRECTORY, '..', '..', 'files') )
REPO_FILES_ROOT = PERSISTENT_FILESTORE
QUOTE_FILES_ROOT = os.path.join(PERSISTENT_FILESTORE, 'quotes')
MADAS_SESSION_TIMEOUT = 1800 #30 minute session timeout

#Ensure the persistent storage dir exits. If it doesn't, exit noisily.
assert os.path.exists(PERSISTENT_FILESTORE), "This application cannot start: It expects a writeable directory at %s to use as a persistent filestore" % (PERSISTENT_FILESTORE) 

# email server
EMAIL_APP_NAME = "Madas (Mango)"
EMAIL_SUBJECT_PREFIX = "Madas (Mango) PROD_SERVER"


#functions to evaluate for status checking
from status_checks import *
STATUS_CHECKS = [check_default]

APPEND_SLASH = True
SITE_NAME = 'madas'
RETURN_EMAIL = 'no-reply@ccg.murdoch.edu.au'

# these are non-standard and override defaults
MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY,"static")
MEDIA_URL = '/static/'
