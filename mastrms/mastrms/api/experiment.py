from rest_framework import serializers, viewsets

from ..repository.models import PlantInfo, MicrobialInfo
from ..repository.models import Experiment, ExperimentStatus
from ..repository.models import OrganismType, BiologicalSource, Organ
from ..repository.models import InstrumentMethod

from .base import router
from .repository import ProjectSerializer, InvestigationSerializer
from .users import UserSerializer

class ExperimentStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExperimentStatus

class ExperimentStatusViewSet(viewsets.ModelViewSet):
    queryset = ExperimentStatus.objects.order_by("name")
    serializer_class = ExperimentStatusSerializer

class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Experiment
        # exclude = ("instrument_method",)  # fixme
    # project = ProjectSerializer(read_only=True)
    # investigation = InvestigationSerializer(read_only=True)
    # users = UserSerializer(many=True, read_only=True)

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


router.register(r'experiment', ExperimentViewSet)
router.register(r'experimentstatus', ExperimentStatusViewSet)
router.register(r'biologicalsource', BiologicalSourceViewSet)
router.register(r'organismtype', OrganismTypeViewSet)
router.register(r'instrumentmethod', InstrumentMethodViewSet)
router.register(r'plantinfo', PlantInfoViewSet)
router.register(r'MicrobialInfo', MicrobialInfoViewSet)
router.register(r'organ', OrganViewSet)
