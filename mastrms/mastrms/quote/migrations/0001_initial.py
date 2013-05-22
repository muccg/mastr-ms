# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Emailmap'
        db.create_table(u'emailmap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emailaddress', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('quote', ['Emailmap'])

        # Adding model 'Quoterequest'
        db.create_table(u'quoterequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emailaddressid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quote.Emailmap'], db_column='emailaddressid')),
            ('tonode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('requesttime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('unread', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('officephone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('attachment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('quote', ['Quoterequest'])

        # Adding model 'Formalquote'
        db.create_table(u'formalquote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quoterequestid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quote.Quoterequest'], db_column='quoterequestid')),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fromemail', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('toemail', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=20)),
            ('downloaded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('purchase_order_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('quote', ['Formalquote'])

        # Adding model 'Quotehistory'
        db.create_table(u'quotehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quoteid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quote.Quoterequest'], db_column='quoteid')),
            ('authoremailid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quote.Emailmap'], db_column='authoremailid')),
            ('newnode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('oldnode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('oldcompleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('changetimestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('quote', ['Quotehistory'])

        # Adding model 'Organisation'
        db.create_table(u'm_organisation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abn', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('quote', ['Organisation'])

        # Adding model 'UserOrganisation'
        db.create_table('m_userorganisation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('organisation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quote.Organisation'])),
        ))
        db.send_create_signal('quote', ['UserOrganisation'])


    def backwards(self, orm):

        # Deleting model 'Emailmap'
        db.delete_table(u'emailmap')

        # Deleting model 'Quoterequest'
        db.delete_table(u'quoterequest')

        # Deleting model 'Formalquote'
        db.delete_table(u'formalquote')

        # Deleting model 'Quotehistory'
        db.delete_table(u'quotehistory')

        # Deleting model 'Organisation'
        db.delete_table(u'm_organisation')

        # Deleting model 'UserOrganisation'
        db.delete_table('m_userorganisation')


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
        'quote.organisation': {
            'Meta': {'object_name': 'Organisation', 'db_table': "u'm_organisation'"},
            'abn': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['quote.UserOrganisation']", 'symmetrical': 'False'})
        },
        'quote.quotehistory': {
            'Meta': {'object_name': 'Quotehistory', 'db_table': "u'quotehistory'"},
            'authoremailid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quote.Emailmap']", 'db_column': "'authoremailid'"}),
            'changetimestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newnode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'oldcompleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oldnode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quoteid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quote.Quoterequest']", 'db_column': "'quoteid'"})
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
        'quote.userorganisation': {
            'Meta': {'object_name': 'UserOrganisation', 'db_table': "'m_userorganisation'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quote.Organisation']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['quote']
