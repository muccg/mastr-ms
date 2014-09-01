import datetime
import logging

from django.db.models import get_app, get_models, Q
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tastypie.api import Api
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, Resource, Bundle
from tastypie.fields import DictField
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpGone, HttpMultipleChoices
from tastypie.utils import trailing_slash
import tastypie.constants


from .repository.models import Project, Investigation, Experiment, UserExperiment, ExperimentStatus
from .users.models import User

__all__ = ["api"]

logger = logging.getLogger(__name__)

v1 = Api(api_name="v1")
api = v1


def register(cls):
    "Resource decorator to register it with our v1 api"
    v1.register(cls())
    return cls


class BaseResource(ModelResource):
    class Meta:
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        always_return_data = True

    def get_model(self):
        return self.Meta.queryset.model

    def hydrate(self, bundle):
        # extjs bounces back resources the same way it received them
        if "objects" in bundle.data:
            bundle.data = bundle.data["objects"]
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        # extjs likes to have success and msg kind of stuff
        data["_success"] = True
        data["_msg"] = ""
        return data

    def alter_detail_data_to_serialize(self, request, data):
        # extjs likes to have success and msg kind of stuff.
        # also post detail and list endpoints must have the same root
        # attribute ("objects").
        return {
            "objects": data,
            "_success": True,
            "_msg": "",
        }


@register
class UserResource(BaseResource):
    class Meta(BaseResource.Meta):
        queryset = User.objects.all().select_related("group")
        fields = ['id', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff']


def get_user_projects(user, qs=None):
    qs = qs or Project.objects.all()
    if not user.is_superuser:
        user_experiments = UserExperiment.objects.filter(user=user)
        qs = qs.filter(Q(managers=user.id) |
                       Q(client=user.id) |
                       Q(id__in=user_experiments.values_list("experiment__project")))
    return qs


@register
class ProjectResource(BaseResource):
    class Meta(BaseResource.Meta):
        queryset = Project.objects.all()

    def get_object_list(self, request):
        qs = super(ProjectResource, self).get_object_list(request)
        return get_user_projects(request.user, qs)


@register
class ExperimentStatusResource(BaseResource):
    class Meta(BaseResource.Meta):
        queryset = ExperimentStatus.objects.all()
        ordering = ["name"]


@register
class InvestigationResource(BaseResource):
    project = fields.ForeignKey(ProjectResource, "project", full=False)

    class Meta(BaseResource.Meta):
        queryset = Investigation.objects.all()

    # def get_object_list(self, request):
    #     qs = super(InvestigationResource, self).get_object_list(request)
    #     projects = get_user_projects(request.user)
    #     return qs.filter(project__in=projects)


@register
class ExperimentResource(BaseResource):
    project = fields.ForeignKey(ProjectResource, "project")
    users = fields.ToManyField(UserResource, "users", null=True)
    status = fields.ForeignKey(ExperimentStatusResource, "status", full=True, null=True)
    investigation = fields.ForeignKey(InvestigationResource, "investigation", full=True, null=True)

    class Meta(BaseResource.Meta):
        queryset = Experiment.objects.all()

    def get_object_list(self, request):
        qs = super(ExperimentResource, self).get_object_list(request)
        if not request.user.is_superuser:
            # fixme: maybe add in client and managers to access list
            qs = qs.filter(users=request.user)
        return qs


@register
class SessionResource(BaseResource):
    """
    This API resource handles user login and logout.
    fixme: put it in ccg-django-utils
    """
    class Meta(BaseResource.Meta):
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser',
                  'tokenless_login_allowed', 'first_name', 'last_name']
        allowed_methods = ['get', 'post']
        resource_name = 'session'
        queryset = User.objects.all()

    def get_object_list(self, request):
        return super(SessionResource, self).get_object_list(request).filter(id=request.user.id)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def _get_data(self, request):
        format = request.META.get('CONTENT_TYPE', 'application/json')
        return self.deserialize(request, request.body, format=format)

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self._get_data(request)

        username = data.get('username', '')
        password = data.get('password', '')
        token = str(data.get('token', '')).strip()

        user = authenticate(username=username, password=password, session=request.session, token=token)

        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True,
                })
            else:
                return self.create_response(
                    request, {
                        'success': False,
                        'reason': 'disabled',
                    },
                    HttpForbidden)
        else:
            return self.create_response(
                request, {
                    'success': False,
                    'reason': 'incorrect' if token or not username or not password else 'token',
                }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)
