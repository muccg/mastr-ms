# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserDetail'
        db.delete_table(u'users_userdetail')


        # Changing field 'User.title'
        db.alter_column(u'users_user', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.commonName'
        db.alter_column(u'users_user', 'commonName', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.mail'
        db.alter_column(u'users_user', 'mail', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.postalAddress'
        db.alter_column(u'users_user', 'postalAddress', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.passwordResetKey'
        db.alter_column(u'users_user', 'passwordResetKey', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.description'
        db.alter_column(u'users_user', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.homePhone'
        db.alter_column(u'users_user', 'homePhone', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.telephoneNumber'
        db.alter_column(u'users_user', 'telephoneNumber', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.registeredAddress'
        db.alter_column(u'users_user', 'registeredAddress', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.physicalDeliveryOfficeName'
        db.alter_column(u'users_user', 'physicalDeliveryOfficeName', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.businessCategory'
        db.alter_column(u'users_user', 'businessCategory', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.carLicense'
        db.alter_column(u'users_user', 'carLicense', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.sn'
        db.alter_column(u'users_user', 'sn', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.givenName'
        db.alter_column(u'users_user', 'givenName', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'User.destinationIndicator'
        db.alter_column(u'users_user', 'destinationIndicator', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

    def backwards(self, orm):
        # Adding model 'UserDetail'
        db.create_table(u'users_userdetail', (
            ('telephoneNumber', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('passwordResetKey', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('physicalDeliveryOfficeName', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('businessCategory', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('registeredAddress', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.User'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('commonName', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('carLicense', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('mail', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('postalAddress', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('givenName', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('homePhone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('destinationIndicator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'users', ['UserDetail'])


        # Changing field 'User.title'
        db.alter_column(u'users_user', 'title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.commonName'
        db.alter_column(u'users_user', 'commonName', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.mail'
        db.alter_column(u'users_user', 'mail', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.postalAddress'
        db.alter_column(u'users_user', 'postalAddress', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.passwordResetKey'
        db.alter_column(u'users_user', 'passwordResetKey', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.description'
        db.alter_column(u'users_user', 'description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.homePhone'
        db.alter_column(u'users_user', 'homePhone', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.telephoneNumber'
        db.alter_column(u'users_user', 'telephoneNumber', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.registeredAddress'
        db.alter_column(u'users_user', 'registeredAddress', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.physicalDeliveryOfficeName'
        db.alter_column(u'users_user', 'physicalDeliveryOfficeName', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.businessCategory'
        db.alter_column(u'users_user', 'businessCategory', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.carLicense'
        db.alter_column(u'users_user', 'carLicense', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.sn'
        db.alter_column(u'users_user', 'sn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.givenName'
        db.alter_column(u'users_user', 'givenName', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'User.destinationIndicator'
        db.alter_column(u'users_user', 'destinationIndicator', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

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
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'businessCategory': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'carLicense': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'commonName': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'destinationIndicator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'givenName': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'homePhone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'passwordResetKey': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'physicalDeliveryOfficeName': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postalAddress': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registeredAddress': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['users']