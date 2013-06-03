# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('lpp_app_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('lpp_app', ['UserProfile'])

        # Adding model 'Osada'
        db.create_table('lpp_app_osada', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lpp_app.UserProfile'], unique=True)),
            ('budzet', self.gf('django.db.models.fields.IntegerField')(default=5000, null=True)),
            ('rozwoj', self.gf('django.db.models.fields.IntegerField')(default=2, null=True)),
            ('data_powstania', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('lpp_app', ['Osada'])

        # Adding model 'Kategoria'
        db.create_table('lpp_app_kategoria', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
        ))
        db.send_create_signal('lpp_app', ['Kategoria'])

        # Adding model 'Obiekt'
        db.create_table('lpp_app_obiekt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('kategoria', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lpp_app.Kategoria'])),
            ('cena', self.gf('django.db.models.fields.IntegerField')()),
            ('poczatkowa_ilosc', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('max_ilosc', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('lpp_app', ['Obiekt'])

        # Adding model 'OsadaObiekt'
        db.create_table('lpp_app_osadaobiekt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('osada', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lpp_app.Osada'])),
            ('obiekt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lpp_app.Obiekt'])),
            ('ilosc', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('lpp_app', ['OsadaObiekt'])

        # Adding unique constraint on 'OsadaObiekt', fields ['osada', 'obiekt']
        db.create_unique('lpp_app_osadaobiekt', ['osada_id', 'obiekt_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'OsadaObiekt', fields ['osada', 'obiekt']
        db.delete_unique('lpp_app_osadaobiekt', ['osada_id', 'obiekt_id'])

        # Deleting model 'UserProfile'
        db.delete_table('lpp_app_userprofile')

        # Deleting model 'Osada'
        db.delete_table('lpp_app_osada')

        # Deleting model 'Kategoria'
        db.delete_table('lpp_app_kategoria')

        # Deleting model 'Obiekt'
        db.delete_table('lpp_app_obiekt')

        # Deleting model 'OsadaObiekt'
        db.delete_table('lpp_app_osadaobiekt')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lpp_app.kategoria': {
            'Meta': {'object_name': 'Kategoria'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'lpp_app.obiekt': {
            'Meta': {'object_name': 'Obiekt'},
            'cena': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kategoria': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lpp_app.Kategoria']"}),
            'max_ilosc': ('django.db.models.fields.IntegerField', [], {}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'poczatkowa_ilosc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        'lpp_app.osada': {
            'Meta': {'object_name': 'Osada'},
            'budzet': ('django.db.models.fields.IntegerField', [], {'default': '5000', 'null': 'True'}),
            'data_powstania': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'rozwoj': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lpp_app.UserProfile']", 'unique': 'True'})
        },
        'lpp_app.osadaobiekt': {
            'Meta': {'unique_together': "(('osada', 'obiekt'),)", 'object_name': 'OsadaObiekt'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilosc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'obiekt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lpp_app.Obiekt']"}),
            'osada': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lpp_app.Osada']"})
        },
        'lpp_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['lpp_app']