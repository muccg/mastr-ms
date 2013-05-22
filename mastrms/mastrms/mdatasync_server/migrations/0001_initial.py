# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'NodeClient'
        db.create_table('mdatasync_server_nodeclient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organisation_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('station_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('default_data_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('hostname', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('flags', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mdatasync_server', ['NodeClient'])

        # Adding model 'NodeRules'
        db.create_table('mdatasync_server_noderules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mdatasync_server.NodeClient'])),
            ('rule_category', self.gf('django.db.models.fields.IntegerField')()),
            ('rule_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('mdatasync_server', ['NodeRules'])


    def backwards(self, orm):

        # Deleting model 'NodeClient'
        db.delete_table('mdatasync_server_nodeclient')

        # Deleting model 'NodeRules'
        db.delete_table('mdatasync_server_noderules')


    models = {
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
        'mdatasync_server.noderules': {
            'Meta': {'object_name': 'NodeRules'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mdatasync_server.NodeClient']"}),
            'rule_category': ('django.db.models.fields.IntegerField', [], {}),
            'rule_text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['mdatasync_server']
