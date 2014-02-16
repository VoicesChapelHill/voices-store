# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.slug'
        db.add_column('store_product', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='changeme', max_length=40),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.slug'
        db.delete_column('store_product', 'slug')


    models = {
        'accounting.account': {
            'Meta': {'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'accounting.klass': {
            'Meta': {'object_name': 'Klass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'store.price': {
            'Meta': {'object_name': 'Price'},
            'amount': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'store.product': {
            'Meta': {'object_name': 'Product'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.Account']"}),
            'blurb': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounting.Klass']"}),
            'member_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['store.Price']"}),
            'pricing': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'quantifiable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sell_start': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'sell_stop': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'special_instructions_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['store']