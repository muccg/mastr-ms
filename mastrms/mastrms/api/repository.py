import re
from django.db.models import Q
from rest_framework import serializers, viewsets, permissions

from ..repository.models import Project, UserExperiment, Investigation

from .base import router


def get_user_projects(user, qs=None):
    qs = qs or Project.objects.all()
    if user.is_anonymous():
        qs = Project.objects.none()
    elif not user.is_superuser:
        user_experiments = UserExperiment.objects.filter(user=user)
        project_ids = user_experiments.values_list("experiment__project")
        qs = qs.filter(Q(managers=user.id) |
                       Q(client=user.id) |
                       Q(id__in=project_ids))
    return qs

class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = super(ProjectViewSet, self).get_queryset()
        return get_user_projects(self.request.user, qs)

class HyperlinkedPrimaryKeyRelatedField(serializers.HyperlinkedRelatedField):
    "Allows posting just an object id instead of full url"

    def to_internal_value(self, data):
        if isinstance(data, int) or (isinstance(data, str) and re.match(r"^\d+$", data)):
            lookup_kwargs = { self.lookup_field: data }
            return self.get_queryset().get(**lookup_kwargs)
            # try:
            #     return self.get_object(self.view_name, (), {self.lookup_field: str(data)})
            # except (ObjectDoesNotExist, TypeError, ValueError):
            #     self.fail('does_not_exist')
        return super(HyperlinkedPrimaryKeyRelatedField, self).to_internal_value(data)

class InvestigationSerializer(serializers.HyperlinkedModelSerializer):
    project = HyperlinkedPrimaryKeyRelatedField(view_name="project-detail", queryset=Project.objects.all())
    class Meta:
        model = Investigation
        fields = ('id', 'url', 'project', 'title', 'description')

class InvestigationViewSet(viewsets.ModelViewSet):
    queryset = Investigation.objects.all()
    serializer_class = InvestigationSerializer
    filter_fields = ("project",)

    def get_queryset(self):
        qs = super(InvestigationViewSet, self).get_queryset()
        projects = get_user_projects(self.request.user)
        return qs.filter(project__in=projects)

router.register(r'project', ProjectViewSet)
router.register(r'investigation', InvestigationViewSet)
