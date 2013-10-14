# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from mastrms.repository.runbuilder import RunBuilder
from mastrms.repository.models import RUN_STATES

class Migration(DataMigration):

    def forwards(self, orm):
        "Sanitize filenames for the incomplete samples of incomplete runs."
        incomplete = orm.RunSample.objects.filter(complete=False).exclude(run__state=RUN_STATES.COMPLETE[0])
        checked = 0
        changed = 0
        for sample in incomplete:
            old = sample.filename
            sample.filename = RunBuilder.sanitize_filename(old)
            if old != sample.filename:
                sample.save()
                changed += 1
            checked += 1
        print "Checked filenames of %d samples, changed %d." % (checked, changed)

    def backwards(self, orm):
        "No way back."




    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mdatasync_server.nodeclient': {
            'Meta': {'object_name': 'NodeClient'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_data_path': ('django.db.models.fields.CharField', [], {'default': "'/usr/local/src/mastrms/scratch/files'", 'max_length': '255'}),
            'flags': ('django.db.models.fields.CharField', [], {'default': "'--protocol=30 -rzv --chmod=ug=rwX'", 'max_length': '255'}),
            'hostname': ('django.db.models.fields.CharField', [], {'default': "u'vmdev.ccg.murdoch.edu.au'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organisation_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'station_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "'apache'", 'max_length': '255'})
        },
        u'quote.emailmap': {
            'Meta': {'object_name': 'Emailmap', 'db_table': "u'emailmap'"},
            'emailaddress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'quote.formalquote': {
            'Meta': {'object_name': 'Formalquote', 'db_table': "u'formalquote'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fromemail': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purchase_order_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quoterequestid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quote.Quoterequest']", 'db_column': "'quoterequestid'"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '20'}),
            'toemail': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'quote.quoterequest': {
            'Meta': {'object_name': 'Quoterequest', 'db_table': "u'quoterequest'"},
            'attachment': ('django.db.models.fields.TextField', [], {}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'emailaddressid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quote.Emailmap']", 'db_column': "'emailaddressid'"}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'officephone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'requesttime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tonode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'repository.animalinfo': {
            'Meta': {'object_name': 'AnimalInfo'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parental_line': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "u'U'", 'max_length': '2'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.BiologicalSource']"})
        },
        u'repository.biologicalsource': {
            'Meta': {'object_name': 'BiologicalSource'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'ncbi_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.OrganismType']"})
        },
        u'repository.clientfile': {
            'Meta': {'object_name': 'ClientFile'},
            'downloaded': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            'filepath': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sharedby': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'sharetimestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'repository.component': {
            'Meta': {'object_name': 'Component'},
            'component_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.ComponentGroup']"}),
            'filename_prefix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sample_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'repository.componentgroup': {
            'Meta': {'object_name': 'ComponentGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'repository.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'formal_quote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quote.Formalquote']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument_method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.InstrumentMethod']", 'null': 'True', 'blank': 'True'}),
            'job_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Project']"}),
            'sample_preparation_notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.ExperimentStatus']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['users.User']", 'null': 'True', 'through': u"orm['repository.UserExperiment']", 'blank': 'True'})
        },
        u'repository.experimentstatus': {
            'Meta': {'object_name': 'ExperimentStatus'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'repository.humaninfo': {
            'Meta': {'object_name': 'HumanInfo'},
            'bmi': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'diagnosis': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '2'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.BiologicalSource']"})
        },
        u'repository.instrumentmethod': {
            'Meta': {'object_name': 'InstrumentMethod'},
            'blank_at_end': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blank_at_start': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'blank_position': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method_path': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'obsolescence_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'obsolete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'randomisation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'csv'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '255'})
        },
        u'repository.instrumentsop': {
            'Meta': {'object_name': 'InstrumentSOP'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'split_size': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'split_threshhold': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trays_max': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'vials_per_tray': ('django.db.models.fields.PositiveIntegerField', [], {'default': '98'})
        },
        u'repository.microbialinfo': {
            'Meta': {'object_name': 'MicrobialInfo'},
            'agitation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'culture_collection_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fermentation_mode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fermentation_vessel': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fermentation_volume': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'gas_delivery_method': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gas_flow_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'gas_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'innoculation_density': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'media': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ph': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.BiologicalSource']"}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        },
        u'repository.organ': {
            'Meta': {'object_name': 'Organ'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'repository.organismtype': {
            'Meta': {'object_name': 'OrganismType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'repository.plantinfo': {
            'Meta': {'object_name': 'PlantInfo'},
            'day_temp_cels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'development_stage': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'growing_place': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'harvested_at': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'harvested_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lamp_details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'light_fluence': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'light_hrs_per_day': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'light_source': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'night_temp_cels': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seeded_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.BiologicalSource']"}),
            'transplated_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'repository.project': {
            'Meta': {'object_name': 'Project'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'managers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'managed_projects'", 'symmetrical': 'False', 'to': u"orm['users.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'repository.rulegenerator': {
            'Meta': {'object_name': 'RuleGenerator'},
            'accessibility': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'apply_sweep_rule': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'node': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'previous_version': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.RuleGenerator']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'repository.rulegeneratorendblock': {
            'Meta': {'object_name': 'RuleGeneratorEndBlock'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Component']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.RuleGenerator']"})
        },
        u'repository.rulegeneratorsampleblock': {
            'Meta': {'object_name': 'RuleGeneratorSampleBlock'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Component']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.RuleGenerator']"}),
            'sample_count': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'repository.rulegeneratorstartblock': {
            'Meta': {'object_name': 'RuleGeneratorStartBlock'},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Component']"}),
            'count': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.RuleGenerator']"})
        },
        u'repository.run': {
            'Meta': {'object_name': 'Run'},
            'complete_sample_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_on': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']", 'null': 'True'}),
            'generated_output': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incomplete_sample_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdatasync_server.NodeClient']", 'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.InstrumentMethod']"}),
            'number_of_methods': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'order_of_methods': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rule_generator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.RuleGenerator']", 'null': 'True', 'blank': 'True'}),
            'sample_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'samples': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['repository.Sample']", 'through': u"orm['repository.RunSample']", 'symmetrical': 'False'}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'repository.runsample': {
            'Meta': {'object_name': 'RunSample', 'db_table': "u'repository_run_samples'"},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'component': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['repository.Component']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Run']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Sample']", 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'vial_number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'repository.sample': {
            'Meta': {'object_name': 'Sample'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sample_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.SampleClass']", 'null': 'True', 'blank': 'True'}),
            'sample_class_sequence': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'sample_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'})
        },
        u'repository.sampleclass': {
            'Meta': {'object_name': 'SampleClass'},
            'biological_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.BiologicalSource']", 'null': 'True', 'blank': 'True'}),
            'class_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organ': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Organ']", 'null': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.SampleTimeline']", 'null': 'True', 'blank': 'True'}),
            'treatments': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Treatment']", 'null': 'True', 'blank': 'True'})
        },
        u'repository.samplelog': {
            'Meta': {'object_name': 'SampleLog'},
            'changetimestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Sample']"}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True', 'blank': 'True'})
        },
        u'repository.sampletimeline': {
            'Meta': {'object_name': 'SampleTimeline'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timeline': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'repository.standardoperationprocedure': {
            'Meta': {'object_name': 'StandardOperationProcedure'},
            'area_where_valid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'attached_pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'defined_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'experiments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['repository.Experiment']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'replaces_document': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'repository.treatment': {
            'Meta': {'object_name': 'Treatment'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'repository.userexperiment': {
            'Meta': {'object_name': 'UserExperiment'},
            'additional_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.UserInvolvementType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'repository.userinvolvementtype': {
            'Meta': {'object_name': 'UserInvolvementType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'businessCategory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'carLicense': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'destinationIndicator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'homePhone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'passwordResetKey': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'physicalDeliveryOfficeName': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postalAddress': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registeredAddress': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['repository']
    symmetrical = True
