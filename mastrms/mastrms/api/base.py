import sys
import logging
from tastypie.api import Api
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, Resource, Bundle, Serializer

logger = logging.getLogger(__name__)


v1 = Api(api_name="v1")

def register(cls):
    "Resource decorator to register it with our v1 api"
    v1.register(cls())
    return cls

def make_generic_resource(model_cls, module_name=__name__, paging=True):
    if paging:
        paging_limit = 20
        max_paging_limit = 0
    else:
        paging_limit = 0
        max_paging_limit = 0

    class GenericResource(BaseResource):
        class Meta(BaseResource.Meta):
            queryset = model_cls.objects.all()
            resource_name = model_cls._meta.object_name.lower()
            limit = paging_limit
            max_limit = max_paging_limit
    GenericResource.__name__ = model_cls.__name__ + "Resource"

    resource = GenericResource()
    if resource._meta.resource_name not in v1._canonicals:
        v1.register(resource)
        if module_name in sys.modules:
            setattr(sys.modules[module_name], GenericResource.__name__, GenericResource)
    return GenericResource


class BetterSerializer(Serializer):
    """
    Our own serializer to format datetimes in ISO 8601 but with timezone
    offset. Courtesy of
    http://www.tryolabs.com/Blog/2013/03/16/displaying-timezone-aware-dates-tastypie/
    """
    def format_datetime(self, data):
        # If naive or rfc-2822, default behavior...
        if is_naive(data) or self.datetime_formatting == 'rfc-2822':
            return super(BetterSerializer, self).format_datetime(data)
        return data.isoformat()


class BetterAuthentication(SessionAuthentication):
    """
    Normal Django session authentication plus support for custom
    username fields.
    """
    def get_identifier(self, request):
        if request.user.is_authenticated():
            return super(BetterAuthentication, self).get_identifier(request)
        return ""


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
