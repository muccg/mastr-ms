from rest_framework import serializers, viewsets, fields

from ..repository.models import PlantInfo, MicrobialInfo
from ..repository.models import Experiment, ExperimentStatus
from ..repository.models import UserExperiment, UserInvolvementType
from ..repository.models import OrganismType, BiologicalSource, Organ
from ..repository.models import InstrumentMethod, ClientFile
from ..repository.models import RuleGenerator, NodeClient

from .base import router, URLPathField
from .repository import ProjectSerializer, InvestigationSerializer
from .users import UserSerializer

class ExperimentStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExperimentStatus

class ExperimentStatusViewSet(viewsets.ModelViewSet):
    queryset = ExperimentStatus.objects.order_by("name")
    serializer_class = ExperimentStatusSerializer

class UserExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserExperiment

class UserExperimentViewSet(viewsets.ModelViewSet):
    queryset = UserExperiment.objects.order_by("experiment", "type")
    serializer_class = UserExperimentSerializer

class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment
    # fixme: how to embed the through relation?
    # users = UserExperimentSerializer(many=True, read_only=True)

    files = fields.ListField(child=URLPathField(), source="file_urls")

class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    filter_fields = ("project",)

    def get_queryset(self):
        qs = super(ExperimentViewSet, self).get_queryset()
        if not self.request.user.is_superuser:
            # fixme: maybe add in client and managers to access list
            qs = qs.filter(users=self.request.user)
        return qs


class InstrumentMethodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstrumentMethod

class InstrumentMethodViewSet(viewsets.ModelViewSet):
    queryset = InstrumentMethod.objects.all()
    serializer_class = InstrumentMethodSerializer

class OrganismTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganismType

class OrganismTypeViewSet(viewsets.ModelViewSet):
    queryset = OrganismType.objects.all()
    serializer_class = OrganismTypeSerializer


class BiologicalSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BiologicalSource
    # experiment = fields.ForeignKey(ExperimentResource, "experiment")
    # type = fields.ForeignKey("mastrms.api.repository.OrganismTypeResource",
    #                          "type", full=True)

class BiologicalSourceViewSet(viewsets.ModelViewSet):
    queryset = BiologicalSource.objects.all()
    serializer_class = BiologicalSourceSerializer


class PlantInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantInfo

class PlantInfoViewSet(viewsets.ModelViewSet):
    queryset = PlantInfo.objects.all()
    serializer_class = PlantInfoSerializer

class MicrobialInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MicrobialInfo

class MicrobialInfoViewSet(viewsets.ModelViewSet):
    queryset = MicrobialInfo.objects.all()
    serializer_class = MicrobialInfoSerializer

class OrganSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organ

class OrganViewSet(viewsets.ModelViewSet):
    queryset = Organ.objects.all()
    serializer_class = OrganSerializer
    filter_fields = ("experiment",)

class UserInvolvementTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInvolvementType

class UserInvolvementTypeViewSet(viewsets.ModelViewSet):
    queryset = UserInvolvementType.objects.order_by("id")
    serializer_class = UserInvolvementTypeSerializer

class ClientFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientFile
    file_url = URLPathField()

class ClientFileViewSet(viewsets.ModelViewSet):
    queryset = ClientFile.objects.order_by("id")
    serializer_class = ClientFileSerializer

class RuleGeneratorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RuleGenerator
    # start_block_set = RuleGeneratorStartBlockSerializer(many=True)
    # sample_block_set = RuleGeneratorSampleBlockSerializer(many=True)
    # end_block_set = RuleGeneratorEndBlockSerializer(many=True)

class RuleGeneratorViewSet(viewsets.ModelViewSet):
    queryset = RuleGenerator.objects.all()
    serializer_class = RuleGeneratorSerializer

class NodeClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NodeClient

class NodeClientViewSet(viewsets.ModelViewSet):
    queryset = NodeClient.objects.all()
    serializer_class = NodeClientSerializer

router.register(r'experiment', ExperimentViewSet)
router.register(r'experimentstatus', ExperimentStatusViewSet)
router.register(r'userexperiment', UserExperimentViewSet)
router.register(r'userinvolvementtype', UserInvolvementTypeViewSet)
router.register(r'clientfile', ClientFileViewSet)
router.register(r'biologicalsource', BiologicalSourceViewSet)
router.register(r'organismtype', OrganismTypeViewSet)
router.register(r'instrumentmethod', InstrumentMethodViewSet)
router.register(r'plantinfo', PlantInfoViewSet)
router.register(r'microbialinfo', MicrobialInfoViewSet)
router.register(r'organ', OrganViewSet)
router.register(r'rulegenerator', RuleGeneratorViewSet)
router.register(r'nodeclient', NodeClientViewSet)
