# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PrivacyLevelTranslation'
        db.create_table(u'privacy_privacylevel_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['privacy.PrivacyLevel'])),
        ))
        db.send_create_signal(u'privacy', ['PrivacyLevelTranslation'])

        # Adding unique constraint on 'PrivacyLevelTranslation', fields ['language_code', 'master']
        db.create_unique(u'privacy_privacylevel_translation', ['language_code', 'master_id'])

        # Adding model 'PrivacyLevel'
        db.create_table(u'privacy_privacylevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('clearance_level', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal(u'privacy', ['PrivacyLevel'])

        # Adding model 'PrivacySetting'
        db.create_table(u'privacy_privacysetting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['privacy.PrivacyLevel'])),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'privacy', ['PrivacySetting'])


    def backwards(self, orm):
        # Removing unique constraint on 'PrivacyLevelTranslation', fields ['language_code', 'master']
        db.delete_unique(u'privacy_privacylevel_translation', ['language_code', 'master_id'])

        # Deleting model 'PrivacyLevelTranslation'
        db.delete_table(u'privacy_privacylevel_translation')

        # Deleting model 'PrivacyLevel'
        db.delete_table(u'privacy_privacylevel')

        # Deleting model 'PrivacySetting'
        db.delete_table(u'privacy_privacysetting')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'privacy.privacylevel': {
            'Meta': {'ordering': "['clearance_level']", 'object_name': 'PrivacyLevel'},
            'clearance_level': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'privacy.privacyleveltranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'PrivacyLevelTranslation', 'db_table': "u'privacy_privacylevel_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['privacy.PrivacyLevel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'privacy.privacysetting': {
            'Meta': {'object_name': 'PrivacySetting'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['privacy.PrivacyLevel']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['privacy']