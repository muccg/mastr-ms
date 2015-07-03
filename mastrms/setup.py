import setuptools
import os
from setuptools import setup
from mastrms import VERSION

data_files = {}
start_dir = os.path.dirname(os.path.abspath(__file__))
for package in (
        'app',
        'admin',
        'dashboard',
        'login',
        'mdatasync_server',
        'quote',
        'registration',
        'repository',
        'users'):
    data_files['mastrms.' + package] = []
    os.chdir(os.path.join(start_dir, 'mastrms', package))
    for data_dir in (
            'templates',
            'templatetags',
            'static',
            'migrations',
            'fixtures',
            'views',
            'utils',
            'test'):
        data_files[
            'mastrms.' +
            package].extend(
            [
                os.path.join(
                    subdir,
                    f) for (
                    subdir,
                    dirs,
                    files) in os.walk(data_dir) for f in files])
    os.chdir(start_dir)

setup(name='django-mastrms',
      version=VERSION,
      description='Mastr MS',
      long_description='Django Mastr MS web application',
      author='Centre for Comparative Genomics',
      author_email='web@ccg.murdoch.edu.au',
      packages=[
          'mastrms',
          'mastrms.api',
          'mastrms.app',
          'mastrms.admin',
          'mastrms.dashboard',
          'mastrms.login',
          'mastrms.mdatasync_server',
          'mastrms.mdatasync_server.management',
          'mastrms.mdatasync_server.management.commands',
          'mastrms.quote',
          'mastrms.registration',
          'mastrms.repository',
          'mastrms.users',
          'mastrms.testutils',
      ],
      package_data=data_files,
      zip_safe=False,
      scripts=["scripts/mastrms-manage.py"],
      )
