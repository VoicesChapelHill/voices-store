# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrderLine'
        db.create_table('store_orderline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Product'])),
            ('price', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Price'], null=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2)),
            ('sale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Sale'], null=True)),
        ))
        db.send_create_signal('store', ['OrderLine'])

        # Adding model 'Sale'
        db.create_table('store_sale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('store', ['Sale'])


    def backwards(self, orm):
        # Deleting model 'OrderLine'
        db.delete_table('store_orderline')

        # Deleting model 'Sale'
        db.delete_table('store_sale')


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
        'store.orderline': {
            'Meta': {'object_name': 'OrderLine'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Price']", 'null': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Sale']", 'null': 'True'})
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
        },
        'store.sale': {
            'Meta': {'object_name': 'Sale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['store']