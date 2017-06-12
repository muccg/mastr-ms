from .settings import *

INSTALLED_APPS += [
    'django_nose',
    'lettuce.django',
]

SOUTH_TESTS_MIGRATE = True

TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
