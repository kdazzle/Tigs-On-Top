# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Game'
        db.create_table(u'gameTracker_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usTeam', self.gf('django.db.models.fields.CharField')(default='Tigers', max_length=64)),
            ('themTeam', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('usScore', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('themScore', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('startTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('addDate', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('currentStatus', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
        ))
        db.send_create_signal(u'gameTracker', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Game'
        db.delete_table(u'gameTracker_game')


    models = {
        u'gameTracker.game': {
            'Meta': {'object_name': 'Game'},
            'addDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currentStatus': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'themScore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'themTeam': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'usScore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'usTeam': ('django.db.models.fields.CharField', [], {'default': "'Tigers'", 'max_length': '64'})
        }
    }

    complete_apps = ['gameTracker']