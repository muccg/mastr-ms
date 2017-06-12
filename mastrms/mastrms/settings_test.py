from .settings import *

INSTALLED_APPS += [
    'django_nose',
]

SOUTH_TESTS_MIGRATE = True

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
