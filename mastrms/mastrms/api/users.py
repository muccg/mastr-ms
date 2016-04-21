from rest_framework import serializers, viewsets
from django.contrib.auth.models import Group
from ..users.models import User
from .base import router

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'url', 'email',
                  'is_active', 'is_staff',
                  'last_name', 'first_name')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("group")
    serializer_class = UserSerializer

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'url', 'name')

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
