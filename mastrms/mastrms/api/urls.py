from django.conf.urls import url, include
import rest_framework.authtoken.views

from .base import router

# import modules to cause router registration
from . import experiment
from . import repository
from . import users
from . import sample
from . import dump

urlpatterns = [
    url(r'^', include(router.urls), name="api_root"),
    url(r'^api-token-auth/', rest_framework.authtoken.views.obtain_auth_token),
]
