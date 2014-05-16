import setuptools
import os
from setuptools import setup
from mastrms import VERSION

data_files = {}
start_dir = os.path.dirname(os.path.abspath(__file__))
for package in ('app', 'admin', 'dashboard', 'login', 'mdatasync_server', 'quote', 'registration', 'repository', 'users'):
    data_files['mastrms.' + package] = []
    os.chdir(os.path.join(start_dir, 'mastrms', package))
    for data_dir in ('templates', 'static', 'migrations', 'fixtures', 'views', 'utils'):
        data_files['mastrms.' + package].extend(
            [os.path.join(subdir,f) for (subdir, dirs, files) in os.walk(data_dir) for f in files])
    os.chdir(start_dir)

install_requires = [
    'Django==1.6.4',
    'South==0.8.2',
    'django-extensions>=1.2.5',
    'django-userlog',
    'django-nose',
    'ccg-django-utils',
    'wsgiref==0.1.2',
    'python-memcached==1.48',
    'dingus',
]

dev_requires = [
    'flake8',
    'Werkzeug',
    'django-debug-toolbar',
]

test_requires = [
    'nose',
]

postgres_requires = [
    'psycopg2>=2.5.0,<2.6.0',
]

dependency_links = [
    'https://bitbucket.org/ccgmurdoch/django-userlog/downloads/django_userlog-0.1.tar.gz',
    'https://bitbucket.org/ccgmurdoch/ccg-django-utils/downloads/ccg-django-utils-0.2.0.tar.gz',
]

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
    install_requires=install_requires,
    dependency_links=dependency_links,
    extras_require={
        'test': test_requires,
        'dev': dev_requires,
        'postgres': postgres_requires,
    },
    scripts=["scripts/mastrms-manage.py"],
)
