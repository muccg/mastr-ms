import setuptools
import os
from setuptools import setup
from mastrms import VERSION

data_files = {}
start_dir = os.getcwd()
for package in ('app', 'admin', 'dashboard', 'login', 'mdatasync_server', 'quote', 'registration', 'repository', 'users'):
    data_files['mastrms.' + package] = []
    os.chdir(os.path.join('mastrms', package))
    for data_dir in ('templates', 'static', 'migrations', 'fixtures', 'views', 'utils'):
        data_files['mastrms.' + package].extend(
            [os.path.join(subdir,f) for (subdir, dirs, files) in os.walk(data_dir) for f in files])
    os.chdir(start_dir)

setup(name='django-mastrms',
    version=VERSION,
    description='Mastr MS',
    long_description='Django Mastr MS web application',
    author='Centre for Comparative Genomics',
    author_email='web@ccg.murdoch.edu.au',
    packages=[
        'mastrms',
        'mastrms.app',
        'mastrms.admin',
        'mastrms.dashboard',
        'mastrms.login',
        'mastrms.mdatasync_client',
        'mastrms.mdatasync_client.client',
        'mastrms.mdatasync_client.client.plogging',
        'mastrms.mdatasync_client.client.yaphc',
        'mastrms.mdatasync_client.client.httplib2',
        'mastrms.mdatasync_client.client.tendo',
        'mastrms.mdatasync_client.client.test',
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
    install_requires=[
        'Django',
        'South',
        'ccg-extras',
        'wsgiref',
        'python-memcached',
        'django-userlog',
        'django-extensions',
        'django-nose',
        'dingus',
    ],
    scripts=["scripts/mastrms-manage.py"],
)
