# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Make email field longer and unique
        db.alter_column(u'users_user', 'email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255))
        db.create_index(u'users_user', ['email'])
        db.create_unique(u'users_user', ['email'])

        # Deleting field 'User.username'
        db.delete_column(u'users_user', 'username')

        # Changing field 'User.first_name'
        db.alter_column(u'users_user', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'User.last_name'
        db.alter_column(u'users_user', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):
        # Removing unique constraint on 'User', fields ['email']
        db.delete_unique(u'users_user', ['email'])

        # Removing index on 'User', fields ['email']
        db.delete_index(u'users_user', ['email'])

        # The following code is provided here to aid in writing a correct migration        # Adding field 'User.username'
        db.add_column(u'users_user', 'username',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True),
                      keep_default=False)

        for user in orm['users.User'].objects.all():
            prefix = "%s_" % user.id
            user.username = user.email
            if user.email.startswith(prefix):
                user.email = user.email[len(prefix):]
            user.save()

        # add unique constraint on field 'User.username'
        db.alter_column(u'users_user', 'username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30))

        # Changing field 'User.first_name'
        db.alter_column(u'users_user', 'first_name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'User.last_name'
        db.alter_column(u'users_user', 'last_name', self.gf('django.db.models.fields.CharField')(max_length=30))

        # Changing field 'User.email'
        db.alter_column(u'users_user', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75))

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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'destinationIndicator': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'homePhone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'passwordResetKey': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'physicalDeliveryOfficeName': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postalAddress': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registeredAddress': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephoneNumber': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['users']
