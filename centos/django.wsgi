# Generic WSGI application for use with CCG Django projects
# Installed by RPM package

import os

# snippet to enable the virtualenv
activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin', 'activate_this.py')
if os.path.exists(activate_this):
    exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this))
del activate_this

app_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

# Allow appsettings to be imported
import site
site.addsitedir("/etc/ccgapps")

# setup the settings module for the WSGI app
os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % app_name
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'

import django.core.handlers.wsgi

# This is the WSGI application booter
def application(environ, start):
    if "HTTP_SCRIPT_NAME" in environ:
        environ['SCRIPT_NAME']=environ['HTTP_SCRIPT_NAME']
        os.environ['SCRIPT_NAME']=environ['HTTP_SCRIPT_NAME']
    else:
        os.environ['SCRIPT_NAME']=environ['SCRIPT_NAME']
    if 'DJANGODEV' in environ:
       os.environ['DJANGODEV']=environ['DJANGODEV']
    return django.core.handlers.wsgi.WSGIHandler()(environ,start)
