# -*- mode: python -*-
# Mastr-MS wsgi file
# fixme: make it general and merge with centos/django.wsgi

import os, sys

# activate virtualenv if this a dh-virtualenv package
venv_activate = "/usr/share/python/mastr-ms/bin/activate_this.py"
if os.path.exists(venv_activate):
    execfile(venv_activate, dict(__file__=venv_activate))

webapp_root = os.path.dirname(os.path.abspath(__file__))

# setup the settings module for the WSGI app
from ccg_django_utils.conf import setup_prod_env
setup_prod_env("mastr-ms", config_file="/etc/mastr-ms/database.conf",
               package_name="mastrms")
setup_prod_env("mastr-ms", package_name="mastrms")

os.environ['PROJECT_DIRECTORY'] = webapp_root
os.environ['WEBAPP_ROOT'] = webapp_root
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def application(wenv, start_response):
    # Before entering the django app, transfer the SCRIPT_NAME http
    # header into an environment variable so settings can pick it up.
    mount_point = wenv.get("HTTP_SCRIPT_NAME", wenv.get("SCRIPT_NAME", None))
    if mount_point:
        os.environ["SCRIPT_NAME"] = mount_point
        wenv["HTTP_SCRIPT_NAME"] = wenv["SCRIPT_NAME"] = mount_point
    return _application(wenv, start_response)
