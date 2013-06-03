# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'OrganismType'
        db.create_table('repository_organismtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('repository', ['OrganismType'])

        # Adding model 'BiologicalSource'
        db.create_table('repository_biologicalsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.OrganismType'])),
            ('information', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('ncbi_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['BiologicalSource'])

        # Adding model 'AnimalInfo'
        db.create_table('repository_animalinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.BiologicalSource'])),
            ('sex', self.gf('django.db.models.fields.CharField')(default=u'U', max_length=2)),
            ('age', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('parental_line', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('repository', ['AnimalInfo'])

        # Adding model 'PlantInfo'
        db.create_table('repository_plantinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.BiologicalSource'])),
            ('development_stage', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('growing_place', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('seeded_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('transplated_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('harvested_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('harvested_at', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('night_temp_cels', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('day_temp_cels', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('light_hrs_per_day', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('light_fluence', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2, blank=True)),
            ('light_source', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('lamp_details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['PlantInfo'])

        # Adding model 'HumanInfo'
        db.create_table('repository_humaninfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.BiologicalSource'])),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('bmi', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('diagnosis', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['HumanInfo'])

        # Adding model 'MicrobialInfo'
        db.create_table('repository_microbialinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.BiologicalSource'])),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('culture_collection_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('media', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('fermentation_vessel', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('fermentation_mode', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('innoculation_density', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('fermentation_volume', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('temperature', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('agitation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('ph', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('gas_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('gas_flow_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('gas_delivery_method', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['MicrobialInfo'])

        # Adding model 'Organ'
        db.create_table('repository_organ', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('detail', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['Organ'])

        # Adding model 'ExperimentStatus'
        db.create_table('repository_experimentstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['ExperimentStatus'])

        # Adding model 'Project'
        db.create_table('repository_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['Project'])

        # Adding M2M table for field managers on 'Project'
        db.create_table('repository_project_managers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['repository.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('repository_project_managers', ['project_id', 'user_id'])

        # Adding model 'InstrumentMethod'
        db.create_table('repository_instrumentmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('method_path', self.gf('django.db.models.fields.TextField')()),
            ('method_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_on', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('template', self.gf('django.db.models.fields.TextField')()),
            ('randomisation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blank_at_start', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blank_at_end', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('blank_position', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('obsolete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('obsolescence_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['InstrumentMethod'])

        # Adding model 'Experiment'
        db.create_table('repository_experiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ExperimentStatus'], null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('formal_quote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quote.Formalquote'], null=True, blank=True)),
            ('job_number', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Project'])),
            ('instrument_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.InstrumentMethod'], null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['Experiment'])

        # Adding model 'StandardOperationProcedure'
        db.create_table('repository_standardoperationprocedure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('responsible', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('area_where_valid', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('defined_by', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('replaces_document', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('attached_pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['StandardOperationProcedure'])

        # Adding M2M table for field experiments on 'StandardOperationProcedure'
        db.create_table('repository_standardoperationprocedure_experiments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('standardoperationprocedure', models.ForeignKey(orm['repository.standardoperationprocedure'], null=False)),
            ('experiment', models.ForeignKey(orm['repository.experiment'], null=False))
        ))
        db.create_unique('repository_standardoperationprocedure_experiments', ['standardoperationprocedure_id', 'experiment_id'])

        # Adding model 'Treatment'
        db.create_table('repository_treatment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['Treatment'])

        # Adding model 'SampleTimeline'
        db.create_table('repository_sampletimeline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('timeline', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['SampleTimeline'])

        # Adding model 'SampleClass'
        db.create_table('repository_sampleclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('biological_source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.BiologicalSource'], null=True, blank=True)),
            ('treatments', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Treatment'], null=True, blank=True)),
            ('timeline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.SampleTimeline'], null=True, blank=True)),
            ('organ', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Organ'], null=True, blank=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('repository', ['SampleClass'])

        # Adding model 'Sample'
        db.create_table('repository_sample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sample_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sample_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.SampleClass'], null=True, blank=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('sample_class_sequence', self.gf('django.db.models.fields.SmallIntegerField')(default=1, db_index=True)),
        ))
        db.send_create_signal('repository', ['Sample'])

        # Adding model 'Run'
        db.create_table('repository_run', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'], null=True)),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.InstrumentMethod'])),
            ('created_on', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mdatasync_server.NodeClient'], null=True, blank=True)),
            ('generated_output', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.SmallIntegerField')(default=0, db_index=True)),
            ('sample_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('incomplete_sample_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('complete_sample_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rule_generator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.RuleGenerator'])),
            ('number_of_methods', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('order_of_methods', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['Run'])

        # Adding model 'SampleLog'
        db.create_table('repository_samplelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('changetimestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Sample'])),
        ))
        db.send_create_signal('repository', ['SampleLog'])

        # Adding model 'UserInvolvementType'
        db.create_table('repository_userinvolvementtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('repository', ['UserInvolvementType'])

        # Adding model 'UserExperiment'
        db.create_table('repository_userexperiment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.UserInvolvementType'])),
            ('additional_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['UserExperiment'])

        # Adding model 'RunSample'
        db.create_table(u'repository_run_samples', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Run'])),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Sample'], null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('component', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['repository.Component'])),
            ('sequence', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('vial_number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('method_number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('repository', ['RunSample'])

        # Adding model 'ClientFile'
        db.create_table('repository_clientfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experiment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Experiment'])),
            ('filepath', self.gf('django.db.models.fields.TextField')()),
            ('downloaded', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('sharetimestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sharedby', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('repository', ['ClientFile'])

        # Adding model 'InstrumentSOP'
        db.create_table('repository_instrumentsop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('split_threshhold', self.gf('django.db.models.fields.PositiveIntegerField')(default=20)),
            ('split_size', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
            ('vials_per_tray', self.gf('django.db.models.fields.PositiveIntegerField')(default=98)),
            ('trays_max', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('repository', ['InstrumentSOP'])

        # Adding model 'ComponentGroup'
        db.create_table('repository_componentgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('repository', ['ComponentGroup'])

        # Adding model 'Component'
        db.create_table('repository_component', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sample_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sample_code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('component_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.ComponentGroup'])),
            ('filename_prefix', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('repository', ['Component'])

        # Adding model 'RuleGenerator'
        db.create_table('repository_rulegenerator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('state', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('accessibility', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('previous_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.RuleGenerator'], null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('node', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('repository', ['RuleGenerator'])

        # Adding model 'RuleGeneratorStartBlock'
        db.create_table('repository_rulegeneratorstartblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule_generator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.RuleGenerator'])),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Component'])),
        ))
        db.send_create_signal('repository', ['RuleGeneratorStartBlock'])

        # Adding model 'RuleGeneratorSampleBlock'
        db.create_table('repository_rulegeneratorsampleblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule_generator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.RuleGenerator'])),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sample_count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Component'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('repository', ['RuleGeneratorSampleBlock'])

        # Adding model 'RuleGeneratorEndBlock'
        db.create_table('repository_rulegeneratorendblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule_generator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.RuleGenerator'])),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('count', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('component', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.Component'])),
        ))
        db.send_create_signal('repository', ['RuleGeneratorEndBlock'])


    def backwards(self, orm):

        # Deleting model 'OrganismType'
        db.delete_table('repository_organismtype')

        # Deleting model 'BiologicalSource'
        db.delete_table('repository_biologicalsource')

        # Deleting model 'AnimalInfo'
        db.delete_table('repository_animalinfo')

        # Deleting model 'PlantInfo'
        db.delete_table('repository_plantinfo')

        # Deleting model 'HumanInfo'
        db.delete_table('repository_humaninfo')

        # Deleting model 'MicrobialInfo'
        db.delete_table('repository_microbialinfo')

        # Deleting model 'Organ'
        db.delete_table('repository_organ')

        # Deleting model 'ExperimentStatus'
        db.delete_table('repository_experimentstatus')

        # Deleting model 'Project'
        db.delete_table('repository_project')

        # Removing M2M table for field managers on 'Project'
        db.delete_table('repository_project_managers')

        # Deleting model 'InstrumentMethod'
        db.delete_table('repository_instrumentmethod')

        # Deleting model 'Experiment'
        db.delete_table('repository_experiment')

        # Deleting model 'StandardOperationProcedure'
        db.delete_table('repository_standardoperationprocedure')

        # Removing M2M table for field experiments on 'StandardOperationProcedure'
        db.delete_table('repository_standardoperationprocedure_experiments')

        # Deleting model 'Treatment'
        db.delete_table('repository_treatment')

        # Deleting model 'SampleTimeline'
        db.delete_table('repository_sampletimeline')

        # Deleting model 'SampleClass'
        db.delete_table('repository_sampleclass')

        # Deleting model 'Sample'
        db.delete_table('repository_sample')

        # Deleting model 'Run'
        db.delete_table('repository_run')

        # Deleting model 'SampleLog'
        db.delete_table('repository_samplelog')

        # Deleting model 'UserInvolvementType'
        db.delete_table('repository_userinvolvementtype')

        # Deleting model 'UserExperiment'
        db.delete_table('repository_userexperiment')

        # Deleting model 'RunSample'
        db.delete_table(u'repository_run_samples')

        # Deleting model 'ClientFile'
        db.delete_table('repository_clientfile')

        # Deleting model 'InstrumentSOP'
        db.delete_table('repository_instrumentsop')

        # Deleting model 'ComponentGroup'
        db.delete_table('repository_componentgroup')

        # Deleting model 'Component'
        db.delete_table('repository_component')

        # Deleting model 'RuleGenerator'
        db.delete_table('repository_rulegenerator')

        # Deleting model 'RuleGeneratorStartBlock'
        db.delete_table('repository_rulegeneratorstartblock')

        # Deleting model 'RuleGeneratorSampleBlock'
        db.delete_table('repository_rulegeneratorsampleblock')

        # Deleting model 'RuleGeneratorEndBlock'
        db.delete_table('repository_rulegeneratorendblock')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mdatasync_server.nodeclient': {
            'Meta': {'object_name': 'NodeClient'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_data_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'flags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'hostname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organisation_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'station_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'quote.emailmap': {
            'Meta': {'object_name': 'Emailmap', 'db_table': "u'emailmap'"},
            'emailaddress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'quote.formalquote': {
            'Meta': {'object_name': 'Formalquote', 'db_table': "u'formalquote'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fromemail': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_order_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quoterequestid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quote.Quoterequest']", 'db_column': "'quoterequestid'"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '20'}),
            'toemail': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'quote.quoterequest': {
            'Meta': {'object_name': 'Quoterequest', 'db_table': "u'quoterequest'"},
            'attachment': ('django.db.models.fields.TextField', [], {}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'emailaddressid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quote.Emailmap']", 'db_column': "'emailaddressid'"}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'officephone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'requesttime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tonode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'repository.animalinfo': {
            'Meta': {'object_name': 'AnimalInfo'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'parental_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "u'U'", 'max_length': '2'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.BiologicalSource']"})
        },
        'repository.biologicalsource': {
            'Meta': {'object_name': 'BiologicalSource'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'ncbi_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.OrganismType']"})
        },
        'repository.clientfile': {
            'Meta': {'object_name': 'ClientFile'},
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'filepath': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sharedby': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sharetimestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'repository.component': {
            'Meta': {'object_name': 'Component'},
            'component_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ComponentGroup']"}),
            'filename_prefix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sample_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'repository.componentgroup': {
            'Meta': {'object_name': 'ComponentGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'repository.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'formal_quote': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quote.Formalquote']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.InstrumentMethod']", 'null': 'True', 'blank': 'True'}),
            'job_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Project']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.ExperimentStatus']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'through': "orm['repository.UserExperiment']", 'blank': 'True'})
        },
        'repository.experimentstatus': {
            'Meta': {'object_name': 'ExperimentStatus'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'repository.humaninfo': {
            'Meta': {'object_name': 'HumanInfo'},
            'bmi': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'diagnosis': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.BiologicalSource']"})
        },
        'repository.instrumentmethod': {
            'Meta': {'object_name': 'InstrumentMethod'},
            'blank_at_end': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blank_at_start': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blank_position': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method_path': ('django.db.models.fields.TextField', [], {}),
            'obsolescence_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'obsolete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'randomisation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'repository.instrumentsop': {
            'Meta': {'object_name': 'InstrumentSOP'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'split_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'split_threshhold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trays_max': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'vials_per_tray': ('django.db.models.fields.PositiveIntegerField', [], {'default': '98'})
        },
        'repository.microbialinfo': {
            'Meta': {'object_name': 'MicrobialInfo'},
            'agitation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'culture_collection_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fermentation_mode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fermentation_vessel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fermentation_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'gas_delivery_method': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gas_flow_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'gas_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'innoculation_density': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'media': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ph': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.BiologicalSource']"}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        },
        'repository.organ': {
            'Meta': {'object_name': 'Organ'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'repository.organismtype': {
            'Meta': {'object_name': 'OrganismType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'repository.plantinfo': {
            'Meta': {'object_name': 'PlantInfo'},
            'day_temp_cels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'development_stage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'growing_place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'harvested_at': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'harvested_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lamp_details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'light_fluence': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'light_hrs_per_day': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'light_source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'night_temp_cels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seeded_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.BiologicalSource']"}),
            'transplated_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'repository.project': {
            'Meta': {'object_name': 'Project'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'managed_projects'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'repository.rulegenerator': {
            'Meta': {'object_name': 'RuleGenerator'},
            'accessibility': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'previous_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.RuleGenerator']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'repository.rulegeneratorendblock': {
            'Meta': {'object_name': 'RuleGeneratorEndBlock'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Component']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.RuleGenerator']"})
        },
        'repository.rulegeneratorsampleblock': {
            'Meta': {'object_name': 'RuleGeneratorSampleBlock'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Component']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.RuleGenerator']"}),
            'sample_count': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'repository.rulegeneratorstartblock': {
            'Meta': {'object_name': 'RuleGeneratorStartBlock'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Component']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.RuleGenerator']"})
        },
        'repository.run': {
            'Meta': {'object_name': 'Run'},
            'complete_sample_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']", 'null': 'True'}),
            'generated_output': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incomplete_sample_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mdatasync_server.NodeClient']", 'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.InstrumentMethod']"}),
            'number_of_methods': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_of_methods': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.RuleGenerator']"}),
            'sample_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'samples': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['repository.Sample']", 'through': "orm['repository.RunSample']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'repository.runsample': {
            'Meta': {'object_name': 'RunSample', 'db_table': "u'repository_run_samples'"},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'component': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['repository.Component']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Run']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Sample']", 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'vial_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'repository.sample': {
            'Meta': {'object_name': 'Sample'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sample_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.SampleClass']", 'null': 'True', 'blank': 'True'}),
            'sample_class_sequence': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'sample_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        },
        'repository.sampleclass': {
            'Meta': {'object_name': 'SampleClass'},
            'biological_source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.BiologicalSource']", 'null': 'True', 'blank': 'True'}),
            'class_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organ': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Organ']", 'null': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.SampleTimeline']", 'null': 'True', 'blank': 'True'}),
            'treatments': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Treatment']", 'null': 'True', 'blank': 'True'})
        },
        'repository.samplelog': {
            'Meta': {'object_name': 'SampleLog'},
            'changetimestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Sample']"}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'repository.sampletimeline': {
            'Meta': {'object_name': 'SampleTimeline'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'repository.standardoperationprocedure': {
            'Meta': {'object_name': 'StandardOperationProcedure'},
            'area_where_valid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'attached_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'defined_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'experiments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['repository.Experiment']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'replaces_document': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'repository.treatment': {
            'Meta': {'object_name': 'Treatment'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'repository.userexperiment': {
            'Meta': {'object_name': 'UserExperiment'},
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['repository.UserInvolvementType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'repository.userinvolvementtype': {
            'Meta': {'object_name': 'UserInvolvementType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['repository']
