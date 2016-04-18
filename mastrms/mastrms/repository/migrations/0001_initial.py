# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import mastrms.repository.models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.CharField(default='U', max_length=2, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')])),
                ('age', models.PositiveIntegerField(null=True, blank=True)),
                ('parental_line', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Animal information',
            },
        ),
        migrations.CreateModel(
            name='BiologicalSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(max_length=5)),
                ('information', models.TextField(blank=True)),
                ('ncbi_id', models.PositiveIntegerField(null=True, blank=True)),
                ('label', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filepath', models.TextField()),
                ('downloaded', models.BooleanField(default=False, db_index=True)),
                ('sharetimestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sample_type', models.CharField(max_length=255)),
                ('sample_code', models.CharField(max_length=255)),
                ('filename_prefix', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ComponentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('comment', models.TextField(blank=True)),
                ('created_on', models.DateField(default=datetime.date.today)),
                ('job_number', models.CharField(max_length=30)),
                ('sample_preparation_notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Experiment statuses',
            },
        ),
        migrations.CreateModel(
            name='HumanInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.CharField(default=b'U', max_length=2, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')])),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('bmi', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('diagnosis', models.TextField(blank=True)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Text which will be shown in Mastr-MS', max_length=255)),
                ('method_path', models.CharField(help_text=b'A folder path on the lab machine which will be put in the worklist CSV', max_length=1000)),
                ('method_name', models.CharField(help_text=b'Text which will be put in the worklist', max_length=255)),
                ('version', models.CharField(default=b'1', max_length=255)),
                ('created_on', models.DateField(default=datetime.date.today)),
                ('template', models.CharField(default=b'csv', help_text=b'Determines the worklist format', max_length=10, choices=[(b'csv', b'CSV')])),
                ('randomisation', models.BooleanField(default=False, help_text=b'Unused')),
                ('blank_at_start', models.BooleanField(default=False, help_text=b'Unused')),
                ('blank_at_end', models.BooleanField(default=False, help_text=b'Unused')),
                ('blank_position', models.CharField(help_text=b'Unused', max_length=255, blank=True)),
                ('obsolete', models.BooleanField(default=False, help_text=b'Unused')),
                ('obsolescence_date', models.DateField(help_text=b'Unused', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentSOP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
                ('split_threshhold', models.PositiveIntegerField(default=20)),
                ('split_size', models.PositiveIntegerField(default=10)),
                ('vials_per_tray', models.PositiveIntegerField(default=98)),
                ('trays_max', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Investigation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MicrobialInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genus', models.CharField(max_length=255, blank=True)),
                ('species', models.CharField(max_length=255, blank=True)),
                ('culture_collection_id', models.CharField(max_length=255, blank=True)),
                ('media', models.CharField(max_length=255, blank=True)),
                ('fermentation_vessel', models.CharField(max_length=255, blank=True)),
                ('fermentation_mode', models.CharField(max_length=255, blank=True)),
                ('innoculation_density', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('fermentation_volume', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('temperature', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('agitation', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('ph', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('gas_type', models.CharField(max_length=255, blank=True)),
                ('gas_flow_rate', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('gas_delivery_method', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('abbreviation', models.CharField(max_length=5)),
                ('detail', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganismType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PlantInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('development_stage', models.CharField(max_length=255, blank=True)),
                ('location', models.CharField(max_length=255, blank=True)),
                ('growing_place', models.CharField(max_length=255, blank=True)),
                ('seeded_on', models.DateField(null=True, blank=True)),
                ('transplated_on', models.DateField(null=True, blank=True)),
                ('harvested_on', models.DateField(null=True, blank=True)),
                ('harvested_at', models.TimeField(null=True, blank=True)),
                ('night_temp_cels', models.PositiveIntegerField(null=True, blank=True)),
                ('day_temp_cels', models.PositiveIntegerField(null=True, blank=True)),
                ('light_hrs_per_day', models.DecimalField(null=True, max_digits=4, decimal_places=2, blank=True)),
                ('light_fluence', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('light_source', models.TextField(blank=True)),
                ('lamp_details', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Plant information',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('created_on', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='RuleGenerator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('state', models.PositiveIntegerField(default=1, choices=[(1, b'In Design'), (2, b'Enabled'), (3, b'Disabled')])),
                ('accessibility', models.PositiveIntegerField(default=1, choices=[(1, b'Only Myself'), (2, b'Everyone in Node'), (3, b'Everyone')])),
                ('apply_sweep_rule', models.BooleanField(default=True)),
                ('version', models.PositiveIntegerField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('node', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RuleGeneratorEndBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RuleGeneratorSampleBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField()),
                ('sample_count', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
                ('order', models.PositiveIntegerField(choices=[(1, b'random'), (2, b'position')])),
            ],
        ),
        migrations.CreateModel(
            name='RuleGeneratorStartBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateField(default=datetime.date.today)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('generated_output', models.TextField(blank=True)),
                ('state', models.SmallIntegerField(default=0, db_index=True, choices=[(0, 'New'), (1, 'In Progress'), (2, 'Complete')])),
                ('sample_count', models.IntegerField(default=0)),
                ('incomplete_sample_count', models.IntegerField(default=0)),
                ('complete_sample_count', models.IntegerField(default=0)),
                ('number_of_methods', models.IntegerField(null=True, blank=True)),
                ('order_of_methods', models.IntegerField(blank=True, null=True, choices=[(1, b'resampled vial'), (2, b'individual vial')])),
            ],
        ),
        migrations.CreateModel(
            name='RunSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=255, blank=True)),
                ('complete', models.BooleanField(default=False, db_index=True)),
                ('sequence', models.PositiveIntegerField(default=0)),
                ('vial_number', models.PositiveIntegerField(null=True, blank=True)),
                ('method_number', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'repository_run_samples',
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sample_id', models.CharField(max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('comment', models.TextField(blank=True)),
                ('weight', models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)),
                ('sample_class_sequence', models.SmallIntegerField(default=1, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='SampleClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_id', models.CharField(max_length=255)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Sample classes',
            },
        ),
        migrations.CreateModel(
            name='SampleLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveIntegerField(default=0, choices=[(0, 'Received'), (1, 'Stored'), (2, 'Prepared'), (3, 'Acquired'), (4, 'Data Processed')])),
                ('changetimestamp', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SampleTimeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(max_length=5)),
                ('timeline', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StandardOperationProcedure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('responsible', models.CharField(max_length=255, blank=True)),
                ('label', models.CharField(max_length=255, blank=True)),
                ('area_where_valid', models.CharField(max_length=255, blank=True)),
                ('comment', models.CharField(max_length=255, blank=True)),
                ('organisation', models.CharField(max_length=255, blank=True)),
                ('version', models.CharField(max_length=255, blank=True)),
                ('defined_by', models.CharField(max_length=255, blank=True)),
                ('replaces_document', models.CharField(max_length=255, blank=True)),
                ('content', models.CharField(max_length=255, blank=True)),
                ('attached_pdf', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/rodney/dev/mastr-ms/mastrms/mastrms/scratch/files/sops'), max_length=500, null=True, upload_to=mastrms.repository.models.sop_filepath, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserExperiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_info', models.TextField(blank=True)),
                ('experiment', models.ForeignKey(to='repository.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='UserInvolvementType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='userexperiment',
            name='type',
            field=models.ForeignKey(to='repository.UserInvolvementType'),
        ),
    ]
