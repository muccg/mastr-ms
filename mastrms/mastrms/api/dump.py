from functools import wraps
from django.db.models import Q
from rest_framework import serializers, viewsets, permissions, fields
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request


from .base import router
from .repository import ProjectSerializer, InvestigationSerializer
from .repository import get_user_projects
from .experiment import ExperimentSerializer, ExperimentStatusSerializer
from .experiment import UserInvolvementTypeSerializer, InstrumentMethodSerializer
from .experiment import UserExperimentSerializer
from .experiment import ClientFileSerializer
from .experiment import RuleGeneratorSerializer, NodeClientSerializer
from .experiment import BiologicalSourceSerializer, OrganSerializer, OrganismTypeSerializer
from .sample import SampleSerializer, RunSampleSerializer, RunSerializer
from .sample import SampleClassSerializer, TreatmentSerializer, SampleTimelineSerializer
from .sample import ComponentGroupSerializer, ComponentSerializer
from .users import UserSerializer
from ..repository.models import Project
from ..repository.isatab import ISATabExportView
from ..repository.models import ExperimentStatus, UserInvolvementType
from ..repository.models import UserExperiment, InstrumentMethod
from ..repository.models import Run, RunSample, Sample
from ..repository.models import SampleClass, Treatment, SampleTimeline
from ..repository.models import BiologicalSource, Organ, OrganismType
from ..repository.models import NodeClient, RuleGenerator
from ..repository.models import Component, ComponentGroup
from ..repository.models import ClientFile
from ..users.models import User


class DumpProject(Project):
    class Meta:
        proxy = True

    @property
    def samples(self):
        return Sample.objects.filter(experiment__project=self)

    @property
    def sample_class(self):
        return SampleClass.objects.filter(id__in=self.samples.values_list("sample_class"))

    @property
    def sample_timeline(self):
        return SampleTimeline.objects.filter(id__in=self.sample_class.values_list("timeline"))

    @property
    def organ(self):
        return Organ.objects.filter(id__in=self.sample_class.values_list("organ"))

    @property
    def biological_source(self):
        return BiologicalSource.objects.filter(id__in=self.sample_class.values_list("biological_source"))

    @property
    def users(self):
        "All users which are related to this experiment"
        return User.objects.filter(Q(id__in=self.experiment_set.values_list("users")) |
                                   Q(id__in=self.managers.values_list("id")) |
                                   Q(id=self.client.id) |
                                   Q(id__in=self.rule_generator.values_list("created_by")) |
                                   Q(id__in=self.runs.values_list("creator")) |
                                   Q(id__in=self.instrument_method.values_list("creator")))

    @property
    def user_experiment(self):
        "Experiment users (investigators/clients/managers/etc)"
        # fixme: should be embeddeded in ExperimentSerializer
        return UserExperiment.objects.filter(experiment__in=self.experiment_set.all())

    @property
    def instrument_method(self):
        "Instrument methods used by experiments"
        return InstrumentMethod.objects.filter(id__in=self.experiment_set.values_list("instrument_method"))

    @property
    def client_file(self):
        "Experiment files which clients have been granted access to"
        return ClientFile.objects.filter(experiment__in=self.experiment_set.all())

    @property
    def runs(self):
        "Runs of all experiments, contains files"
        return Run.objects.filter(experiment__in=self.experiment_set.all())

    @property
    def nodeclient(self):
        return NodeClient.objects.filter(id__in=self.runs.values_list("machine"))

    @property
    def rule_generator(self):
        return RuleGenerator.objects.filter(id__in=self.runs.values_list("rule_generator"))

    @property
    def run_sample(self):
        return RunSample.objects.filter(run__in=self.runs)

    @property
    def component(self):
        return Component.objects.filter(id__in=self.run_sample.values_list("component"))

    @property
    def experiment_status(self):
        # return ExperimentStatus.objects.all()
        return ExperimentStatus.objects.filter(id__in=self.experiment_set.values_list("status"))

    @property
    def user_involvement_type(self):
        # return UserInvolvementType.objects.all()
        return UserInvolvementType.objects.filter(id__in=self.user_experiment.values_list("type"))

    @property
    def component_group(self):
        return ComponentGroup.objects.filter(id__in=self.run_sample.values_list("component__component_group"))

    @property
    def organism_type(self):
        return OrganismType.objects.filter(id__in=self.biological_source.values_list("type"))

class ProjectDumpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DumpProject

    # model fields
    experiment_set = ExperimentSerializer(many=True)
    investigation_set = InvestigationSerializer(many=True)
    client = UserSerializer()
    managers = UserSerializer(many=True)

    # related info
    samples = SampleSerializer(many=True)
    user_experiment = UserExperimentSerializer(many=True)
    instrument_method = InstrumentMethodSerializer(many=True)
    users = UserSerializer(many=True)
    sample_class = SampleClassSerializer(many=True)
    sample_timeline = SampleTimelineSerializer(many=True)
    organ = OrganSerializer(many=True)
    biological_source = BiologicalSourceSerializer(many=True)

    # all runs in all experiments
    runs = RunSerializer(many=True)
    client_file = ClientFileSerializer(many=True)

    # details about the run
    nodeclient = NodeClientSerializer(many=True)
    rule_generator = RuleGeneratorSerializer(many=True)
    run_sample = RunSampleSerializer(many=True)
    component = ComponentSerializer(many=True)

    # boring drop-down lists
    experiment_status = ExperimentStatusSerializer(many=True)
    user_involvement_type = UserInvolvementTypeSerializer(many=True)
    component_group = ComponentGroupSerializer(many=True)
    organism_type = OrganismTypeSerializer(many=True)

class ProjectDumpViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DumpProject.objects.all()
    serializer_class = ProjectDumpSerializer

    def get_queryset(self):
        qs = super(ProjectDumpViewSet, self).get_queryset()
        return get_user_projects(self.request.user, qs)

router.register(r'dump/project', ProjectDumpViewSet, base_name="dumpproject")
