from tastypie import fields
import tastypie.constants

from ..repository.models import PlantInfo, MicrobialInfo
from ..repository.models import Investigation, Experiment, UserExperiment, ExperimentStatus

from .base import BaseResource, register


@register
class ExperimentStatusResource(BaseResource):
    class Meta(BaseResource.Meta):
        queryset = ExperimentStatus.objects.all()
        ordering = ["name"]


@register
class InvestigationResource(BaseResource):
    project = fields.ForeignKey("mastrms.api.repository.ProjectResource", "project", full=False)

    class Meta(BaseResource.Meta):
        queryset = Investigation.objects.all()

    # def get_object_list(self, request):
    #     qs = super(InvestigationResource, self).get_object_list(request)
    #     projects = get_user_projects(request.user)
    #     return qs.filter(project__in=projects)


@register
class ExperimentResource(BaseResource):
    project = fields.ForeignKey("mastrms.api.repository.ProjectResource", "project")
    users = fields.ToManyField("mastrms.api.users.UserResource", "users", null=True)
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


# @register
class BiologicalSourceResource(BaseResource):
    experiment = fields.ForeignKey(ExperimentResource, "experiment")
    type = fields.ForeignKey("mastrms.api.repository.OrganismTypeResource",
                             "type", full=True)


class SourceInfoResource(BaseResource):
    source = fields.ForeignKey(BiologicalSourceResource, "source")

    class Meta(BaseResource.Meta):
        filtering = {
            "source": tastypie.constants.ALL,
        }


# @register
class PlantInfoResource(SourceInfoResource):
    class Meta(SourceInfoResource.Meta):
        queryset = PlantInfo.objects.all()


# @register
class MicrobialResource(SourceInfoResource):
    class Meta(SourceInfoResource.Meta):
        queryset = MicrobialInfo.objects.all()


# @register
class OrganResource(BaseResource):
    experiment = fields.ForeignKey(ExperimentResource, "experiment")

    class Meta(BaseResource.Meta):
        filtering = {
            "experiment": tastypie.constants.ALL,
        }
