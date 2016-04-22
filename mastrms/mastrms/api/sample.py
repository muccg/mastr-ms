from rest_framework import serializers, viewsets, fields

from ..repository.models import Run, RunSample, Sample
from ..repository.models import SampleClass, Treatment, SampleTimeline
from ..repository.models import Component, ComponentGroup
from ..repository.models import Experiment, Project

from .base import router, URLPathField

class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sample

class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.order_by("id")
    serializer_class = SampleSerializer

class SampleClassSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleClass

class SampleClassViewSet(viewsets.ModelViewSet):
    queryset = SampleClass.objects.order_by("id")
    serializer_class = SampleClassSerializer

class TreatmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Treatment

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.order_by("id")
    serializer_class = TreatmentSerializer

class SampleTimelineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SampleTimeline

class SampleTimelineViewSet(viewsets.ModelViewSet):
    queryset = SampleTimeline.objects.order_by("id")
    serializer_class = SampleTimelineSerializer

class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
    files = fields.ListField(child=URLPathField(), source="file_urls")

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.order_by("id")
    serializer_class = RunSerializer

class RunSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RunSample

class RunSampleViewSet(viewsets.ModelViewSet):
    queryset = RunSample.objects.order_by("id")
    serializer_class = RunSampleSerializer

class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.order_by("id")
    serializer_class = ComponentSerializer

class ComponentGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentGroup

class ComponentGroupViewSet(viewsets.ModelViewSet):
    queryset = ComponentGroup.objects.all()
    serializer_class = ComponentGroupSerializer


router.register(r'sample', SampleViewSet)
router.register(r'sampleclass', SampleClassViewSet)
router.register(r'treatment', TreatmentViewSet)
router.register(r'sampletimeline', SampleTimelineViewSet)
router.register(r'run', RunViewSet)
router.register(r'runsample', RunSampleViewSet)
router.register(r'component', ComponentViewSet)
router.register(r'componentgroup', ComponentGroupViewSet)
