# -*- coding: utf-8 -*-
from django.utils.text import slugify
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for product in orm.Product.objects.filter(slug='changeme'):
            product.slug = slugify(product.name)
            product.save()


    def backwards(self, orm):
        pass

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
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '40'}),
            'special_instructions_prompt': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['store']
    symmetrical = True
