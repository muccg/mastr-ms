import datetime
import logging

from django.db.models import get_app, get_models, Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tastypie import fields
from tastypie.resources import ModelResource, Resource, Bundle
from tastypie.fields import DictField
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpGone, HttpMultipleChoices
import tastypie.constants


from . import app
from . import experiment
from . import repository
from . import users

from .base import v1, make_generic_resource
from .utils import mastrms_apps


logger = logging.getLogger(__name__)

__all__ = ["v1"]


def register_all(app_label):
    for model in get_models(get_app(app_label)):
        module_name = "%s.%s" % (__name__, app_label)
        make_generic_resource(model, module_name=module_name)

# # Might be nice to enable this, but it could leak information
# for appname in mastrms_apps():
#     register_all(appname)
