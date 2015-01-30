from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from tastypie.utils import trailing_slash

from ..users.models import User

from .base import BaseResource, register


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
