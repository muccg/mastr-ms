from django.db.models import Q

from ..repository.models import Project, UserExperiment

from .base import BaseResource, register

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
