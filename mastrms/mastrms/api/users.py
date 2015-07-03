from ..users.models import User

from .base import BaseResource, register


@register
class UserResource(BaseResource):

    class Meta(BaseResource.Meta):
        queryset = User.objects.all().select_related("group")
        fields = ['id', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff']
