#!/usr/bin/env python
import os
import sys
import pwd

production_install = True

if production_install:
    (uid, gid, gecos, homedir) = pwd.getpwnam('apache')[2:6]
    os.setgid(gid)
    os.setuid(uid)
    os.environ["HOME"] = homedir

if __name__ == "__main__":
    if production_install:
        # setup the settings module for the django app
        from mastrms.confutil import setup_prod_env
        setup_prod_env()
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mastrms.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
