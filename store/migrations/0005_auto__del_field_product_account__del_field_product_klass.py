# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Product.account'
        db.delete_column('store_product', 'account_id')

        # Deleting field 'Product.klass'
        db.delete_column('store_product', 'klass_id')


    def backwards(self, orm):
        # Adding field 'Product.account'
        db.add_column('store_product', 'account',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['accounting.Account']),
                      keep_default=False)

        # Adding field 'Product.klass'
        db.add_column('store_product', 'klass',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['accounting.Klass']),
                      keep_default=False)


    models = {
        'store.orderline': {
            'Meta': {'object_name': 'OrderLine'},
            'amount': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': "'0.00'", 'max_digits': '8'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['store.Price']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['store.Sale']"}),
            'special_instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'store.price': {
            'Meta': {'object_name': 'Price'},
            'amount': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        'store.product': {
            'Meta': {'object_name': 'Product'},
            'blurb': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['store.Price']"}),
            'pricing': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'quantifiable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sell_start': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'sell_stop': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'special_instructions_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'store.sale': {
            'Meta': {'object_name': 'Sale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['store']