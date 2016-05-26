# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mdatasync_server', '0001_initial'),
        ('quote', '0002_auto_20160418_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='userexperiment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='treatment',
            name='experiment',
            field=models.ForeignKey(to='repository.Experiment'),
        ),
        migrations.AddField(
            model_name='standardoperationprocedure',
            name='experiments',
            field=models.ManyToManyField(to='repository.Experiment', blank=True),
        ),
        migrations.AddField(
            model_name='sampletimeline',
            name='experiment',
            field=models.ForeignKey(to='repository.Experiment'),
        ),
        migrations.AddField(
            model_name='samplelog',
            name='sample',
            field=models.ForeignKey(to='repository.Sample'),
        ),
        migrations.AddField(
            model_name='samplelog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='sampleclass',
            name='biological_source',
            field=models.ForeignKey(blank=True, to='repository.BiologicalSource', null=True),
        ),
        migrations.AddField(
            model_name='sampleclass',
            name='experiment',
            field=models.ForeignKey(to='repository.Experiment'),
        ),
        migrations.AddField(
            model_name='sampleclass',
            name='organ',
            field=models.ForeignKey(blank=True, to='repository.Organ', null=True),
        ),
        migrations.AddField(
            model_name='sampleclass',
            name='timeline',
            field=models.ForeignKey(blank=True, to='repository.SampleTimeline', null=True),
        ),
        migrations.AddField(
            model_name='sampleclass',
            name='treatments',
            field=models.ForeignKey(blank=True, to='repository.Treatment', null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='experiment',
            field=models.ForeignKey(to='repository.Experiment'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_class',
            field=models.ForeignKey(blank=True, to='repository.SampleClass', null=True),
        ),
        migrations.AddField(
            model_name='runsample',
            name='component',
            field=models.ForeignKey(default=0, to='repository.Component'),
        ),
        migrations.AddField(
            model_name='runsample',
            name='run',
            field=models.ForeignKey(to='repository.Run'),
        ),
        migrations.AddField(
            model_name='runsample',
            name='sample',
            field=models.ForeignKey(blank=True, to='repository.Sample', null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='run',
            name='experiment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='repository.Experiment', null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='mdatasync_server.NodeClient', null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='method',
            field=models.ForeignKey(to='repository.InstrumentMethod'),
        ),
        migrations.AddField(
            model_name='run',
            name='rule_generator',
            field=models.ForeignKey(blank=True, to='repository.RuleGenerator', null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='samples',
            field=models.ManyToManyField(to='repository.Sample', through='repository.RunSample'),
        ),
        migrations.AddField(
            model_name='rulegeneratorstartblock',
            name='component',
            field=models.ForeignKey(to='repository.Component'),
        ),
        migrations.AddField(
            model_name='rulegeneratorstartblock',
            name='rule_generator',
            field=models.ForeignKey(to='repository.RuleGenerator'),
        ),
        migrations.AddField(
            model_name='rulegeneratorsampleblock',
            name='component',
            field=models.ForeignKey(to='repository.Component'),
        ),
        migrations.AddField(
            model_name='rulegeneratorsampleblock',
            name='rule_generator',
            field=models.ForeignKey(to='repository.RuleGenerator'),
        ),
        migrations.AddField(
            model_name='rulegeneratorendblock',
            name='component',
            field=models.ForeignKey(to='repository.Component'),
        ),
        migrations.AddField(
            model_name='rulegeneratorendblock',
            name='rule_generator',
            field=models.ForeignKey(to='repository.RuleGenerator'),
        ),
        migrations.AddField(
            model_name='rulegenerator',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rulegenerator',
            name='previous_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.RuleGenerator', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='managers',
            field=models.ManyToManyField(related_name='managed_projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plantinfo',
            name='source',
            field=models.ForeignKey(to='repository.BiologicalSource'),
        ),
        migrations.AddField(
            model_name='organ',
            name='experiment',
            field=models.ForeignKey(to='repository.Experiment'),
        ),
        migrations.AddField(
            model_name='microbialinfo',
            name='source',
            field=models.ForeignKey(to='repository.BiologicalSource'),
        ),
        migrations.AddField(
            model_name='investigation',
            name='project',
            field=models.ForeignKey(to='repository.Project'),
        ),
        migrations.AddField(
            model_name='instrumentmethod',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='humaninfo',
            name='source',
            field=models.ForeignKey(to='repository.BiologicalSource'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='formal_quote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='quote.Formalquote', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='instrument_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.InstrumentMethod', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='investigation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Investigation', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='project',
            field=models.ForeignKey(to='repository.Project'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.ExperimentStatus', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='repository.UserExperiment', blank=True),
        ),
        migrations.AddField(
            model_name='component',
            name='component_group',
            field=models.ForeignKey(to='repository.ComponentGroup'),
        ),
        migrations.AddField(
            model_name='clientfile',
            name='experiment',
            field=models.ForeignKey(to='repository.Experiment'),
        ),
        migrations.AddField(
            model_name='clientfile',
            name='sharedby',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='biologicalsource',
            name='experiment',
            field=models.ForeignKey(to='repository.Experiment'),
        ),
        migrations.AddField(
            model_name='biologicalsource',
            name='type',
            field=models.ForeignKey(to='repository.OrganismType'),
        ),
        migrations.AddField(
            model_name='animalinfo',
            name='source',
            field=models.ForeignKey(to='repository.BiologicalSource'),
        ),
    ]
