import sys
import logging
from rest_framework import routers, fields

logger = logging.getLogger(__name__)

# extjs can't put with a trailing slash
router = routers.DefaultRouter(trailing_slash=False)


class URLPathField(fields.URLField):
    """
    Source value is an absolute /url/path. This field adds the scheme,
    hostname, port to the front.
    """
    def to_representation(self, urlpath):
        request = self.context.get("request", None)
        return request.build_absolute_uri(urlpath) if request else urlpath
