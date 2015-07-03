from tastypie import fields
import tastypie.constants

from django.db.models import Q

from ..repository.models import Project, UserExperiment, Investigation

from .base import BaseResource, register


def get_user_projects(user, qs=None):
    qs = qs or Project.objects.all()
    if not user.is_superuser:
        user_experiments = UserExperiment.objects.filter(user=user)
        project_ids = user_experiments.values_list("experiment__project")
        qs = qs.filter(Q(managers=user.id) |
                       Q(client=user.id) |
                       Q(id__in=project_ids))
    return qs


@register
class ProjectResource(BaseResource):

    class Meta(BaseResource.Meta):
        queryset = Project.objects.all()

    def get_object_list(self, request):
        qs = super(ProjectResource, self).get_object_list(request)
        return get_user_projects(request.user, qs)


@register
class InvestigationResource(BaseResource):
    project = fields.ForeignKey("mastrms.api.repository.ProjectResource",
                                "project", full=False)

    class Meta(BaseResource.Meta):
        queryset = Investigation.objects.all()
        filtering = {
            "project": tastypie.constants.ALL,
        }

    def get_object_list(self, request):
        qs = super(InvestigationResource, self).get_object_list(request)
        projects = get_user_projects(request.user)
        return qs.filter(project__in=projects)
