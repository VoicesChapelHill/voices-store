# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductGroup'
        db.create_table('store_productgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('display_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('display_end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('store', ['ProductGroup'])

        # Adding M2M table for field to_notify on 'ProductGroup'
        m2m_table_name = db.shorten_name('store_productgroup_to_notify')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productgroup', models.ForeignKey(orm['store.productgroup'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productgroup_id', 'user_id'])

        # Adding model 'Product'
        db.create_table('store_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name1', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name2', self.gf('django.db.models.fields.CharField')(blank=True, max_length=128)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.ProductGroup'], related_name='products')),
        ))
        db.send_create_signal('store', ['Product'])

        # Adding model 'Customer'
        db.create_table('store_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('store', ['Customer'])

        # Adding model 'Sale'
        db.create_table('store_sale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 14, 0, 0))),
            ('who', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Customer'])),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('store', ['Sale'])

        # Adding model 'ItemSale'
        db.create_table('store_itemsale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Product'])),
            ('quantity', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sale', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.Sale'], related_name='items')),
            ('per_item_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal('store', ['ItemSale'])


    def backwards(self, orm):
        # Deleting model 'ProductGroup'
        db.delete_table('store_productgroup')

        # Removing M2M table for field to_notify on 'ProductGroup'
        db.delete_table(db.shorten_name('store_productgroup_to_notify'))

        # Deleting model 'Product'
        db.delete_table('store_product')

        # Deleting model 'Customer'
        db.delete_table('store_customer')

        # Deleting model 'Sale'
        db.delete_table('store_sale')

        # Deleting model 'ItemSale'
        db.delete_table('store_itemsale')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'store.customer': {
            'Meta': {'object_name': 'Customer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'store.itemsale': {
            'Meta': {'object_name': 'ItemSale'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'per_item_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Product']"}),
            'quantity': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Sale']", 'related_name': "'items'"})
        },
        'store.product': {
            'Meta': {'object_name': 'Product'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.ProductGroup']", 'related_name': "'products'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name1': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name2': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'store.productgroup': {
            'Meta': {'object_name': 'ProductGroup'},
            'display_end': ('django.db.models.fields.DateTimeField', [], {}),
            'display_start': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'to_notify': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'store.sale': {
            'Meta': {'object_name': 'Sale'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 14, 0, 0)'}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.Customer']"})
        }
    }

    complete_apps = ['store']