#!/usr/bin/env python
import os
import sys
import pwd

(uid, gid, gecos, homedir) = pwd.getpwnam('apache')[2:6]
os.setgid(gid)
os.setuid(uid)
os.environ["HOME"] = homedir

if __name__ == "__main__":
    # allow importing of appsettings in /etc/ccgapps
    import site
    site.addsitedir("/etc/ccgapps")

    # setup the settings module for the django app
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mastrms.settings')
    os.environ.setdefault('PYTHON_EGG_CACHE', '/tmp/.python-eggs')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
