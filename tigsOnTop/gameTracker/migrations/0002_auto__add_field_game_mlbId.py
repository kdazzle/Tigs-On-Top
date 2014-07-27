# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.mlbId'
        db.add_column(u'gameTracker_game', 'mlbId',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.mlbId'
        db.delete_column(u'gameTracker_game', 'mlbId')


    models = {
        u'gameTracker.game': {
            'Meta': {'object_name': 'Game'},
            'addDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currentStatus': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mlbId': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {}),
            'themScore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'themTeam': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'usScore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'usTeam': ('django.db.models.fields.CharField', [], {'default': "'Tigers'", 'max_length': '64'})
        }
    }

    complete_apps = ['gameTracker']