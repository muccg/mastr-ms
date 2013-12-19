# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NodeClient.samplefile_ext'
        db.add_column(u'mdatasync_server_nodeclient', 'samplefile_ext',
                      self.gf('django.db.models.fields.CharField')(default='.d', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NodeClient.samplefile_ext'
        db.delete_column(u'mdatasync_server_nodeclient', 'samplefile_ext')


    models = {
        u'mdatasync_server.nodeclient': {
            'Meta': {'object_name': 'NodeClient'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_data_path': ('django.db.models.fields.CharField', [], {'default': "'/usr/local/src/mastrms/scratch/files'", 'max_length': '255'}),
            'flags': ('django.db.models.fields.CharField', [], {'default': "'--protocol=30 -rzv --chmod=ug=rwX'", 'max_length': '255'}),
            'hostname': ('django.db.models.fields.CharField', [], {'default': "u'vmdev.ccg.murdoch.edu.au'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'organisation_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'samplefile_ext': ('django.db.models.fields.CharField', [], {'default': "'.d'", 'max_length': '255'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'station_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "'apache'", 'max_length': '255'})
        },
        u'mdatasync_server.noderules': {
            'Meta': {'object_name': 'NodeRules'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mdatasync_server.NodeClient']"}),
            'rule_category': ('django.db.models.fields.IntegerField', [], {}),
            'rule_text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['mdatasync_server']