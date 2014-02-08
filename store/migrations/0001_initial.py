# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table('store_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('blurb', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sell_start', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('sell_stop', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('member_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pricing', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('special_instructions_prompt', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('quantifiable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.Account'])),
            ('klass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounting.Klass'])),
        ))
        db.send_create_signal('store', ['Product'])

        # Adding M2M table for field prices on 'Product'
        m2m_table_name = db.shorten_name('store_product_prices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['store.product'], null=False)),
            ('price', models.ForeignKey(orm['store.price'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'price_id'])

        # Adding model 'Price'
        db.create_table('store_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('store', ['Price'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table('store_product')

        # Removing M2M table for field prices on 'Product'
        db.delete_table(db.shorten_name('store_product_prices'))

        # Deleting model 'Price'
        db.delete_table('store_price')


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
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
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
            'prices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['store.Price']", 'symmetrical': 'False'}),
            'pricing': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'quantifiable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sell_start': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'sell_stop': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'special_instructions_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['store']