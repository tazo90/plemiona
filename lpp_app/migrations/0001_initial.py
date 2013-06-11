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

        # Adding model 'Invites'
        db.create_table('lpp_app_invites', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invites', to=orm['lpp_app.UserProfile'])),
            ('user_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invited', to=orm['lpp_app.UserProfile'])),
        ))
        db.send_create_signal('lpp_app', ['Invites'])

        # Adding unique constraint on 'Invites', fields ['user_from', 'user_to']
        db.create_unique('lpp_app_invites', ['user_from_id', 'user_to_id'])

        # Adding model 'Friends'
        db.create_table('lpp_app_friends', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('lpp_app', ['Friends'])

        # Adding M2M table for field has_friends on 'Friends'
        db.create_table('lpp_app_friends_has_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('friends', models.ForeignKey(orm['lpp_app.friends'], null=False)),
            ('userprofile', models.ForeignKey(orm['lpp_app.userprofile'], null=False))
        ))
        db.create_unique('lpp_app_friends_has_friends', ['friends_id', 'userprofile_id'])

        # Adding model 'Osada'
        db.create_table('lpp_app_osada', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['lpp_app.UserProfile'], unique=True)),
            ('zloto', self.gf('django.db.models.fields.IntegerField')(default=10, null=True)),
            ('drewno', self.gf('django.db.models.fields.IntegerField')(default=200)),
            ('kamien', self.gf('django.db.models.fields.IntegerField')(default=300)),
            ('zelazo', self.gf('django.db.models.fields.IntegerField')(default=80)),
            ('rozwoj', self.gf('django.db.models.fields.IntegerField')(default=2, null=True)),
            ('data_powstania', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('lpp_app', ['Osada'])

        # Adding unique constraint on 'Osada', fields ['nazwa']
        db.create_unique('lpp_app_osada', ['nazwa'])

        # Adding model 'Budynki'
        db.create_table('lpp_app_budynki', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=130, null=True)),
            ('koszt', self.gf('django.db.models.fields.IntegerField')()),
            ('zloto', self.gf('django.db.models.fields.IntegerField')()),
            ('drewno', self.gf('django.db.models.fields.IntegerField')()),
            ('kamien', self.gf('django.db.models.fields.IntegerField')()),
            ('zelazo', self.gf('django.db.models.fields.IntegerField')()),
            ('produktywnosc', self.gf('django.db.models.fields.IntegerField')()),
            ('jednostka_prod', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('max_pojemnosc', self.gf('django.db.models.fields.IntegerField')()),
            ('max_poziom', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('lpp_app', ['Budynki'])

        # Adding model 'Budynki_osada'
        db.create_table('lpp_app_budynki_osada', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('osada', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lpp_app.Osada'], null=True, blank=True)),
            ('budynek', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lpp_app.Budynki'], null=True, blank=True)),
            ('poziom', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('ilosc', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('zloto', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('drewno', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('kamien', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('zelazo', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('produktywnosc', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('produkcja', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('max_pojemnosc', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('lpp_app', ['Budynki_osada'])

        # Adding model 'Armia'
        db.create_table('lpp_app_armia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazwa', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=130, null=True)),
            ('koszt', self.gf('django.db.models.fields.IntegerField')()),
            ('atak', self.gf('django.db.models.fields.IntegerField')()),
            ('obrona', self.gf('django.db.models.fields.IntegerField')()),
            ('zbroja', self.gf('django.db.models.fields.IntegerField')()),
            ('zloto', self.gf('django.db.models.fields.IntegerField')()),
            ('drewno', self.gf('django.db.models.fields.IntegerField')()),
            ('kamien', self.gf('django.db.models.fields.IntegerField')()),
            ('zelazo', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('lpp_app', ['Armia'])

        # Adding model 'Armia_osada'
        db.create_table('lpp_app_armia_osada', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('osada', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lpp_app.Osada'], null=True, blank=True)),
            ('armia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lpp_app.Armia'], null=True, blank=True)),
            ('poziom', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
            ('ilosc', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('zloto', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('drewno', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('kamien', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('zelazo', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal('lpp_app', ['Armia_osada'])

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

        # Removing unique constraint on 'Osada', fields ['nazwa']
        db.delete_unique('lpp_app_osada', ['nazwa'])

        # Removing unique constraint on 'Invites', fields ['user_from', 'user_to']
        db.delete_unique('lpp_app_invites', ['user_from_id', 'user_to_id'])

        # Deleting model 'UserProfile'
        db.delete_table('lpp_app_userprofile')

        # Deleting model 'Invites'
        db.delete_table('lpp_app_invites')

        # Deleting model 'Friends'
        db.delete_table('lpp_app_friends')

        # Removing M2M table for field has_friends on 'Friends'
        db.delete_table('lpp_app_friends_has_friends')

        # Deleting model 'Osada'
        db.delete_table('lpp_app_osada')

        # Deleting model 'Budynki'
        db.delete_table('lpp_app_budynki')

        # Deleting model 'Budynki_osada'
        db.delete_table('lpp_app_budynki_osada')

        # Deleting model 'Armia'
        db.delete_table('lpp_app_armia')

        # Deleting model 'Armia_osada'
        db.delete_table('lpp_app_armia_osada')

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
        'lpp_app.armia': {
            'Meta': {'object_name': 'Armia'},
            'atak': ('django.db.models.fields.IntegerField', [], {}),
            'drewno': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kamien': ('django.db.models.fields.IntegerField', [], {}),
            'koszt': ('django.db.models.fields.IntegerField', [], {}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'obrona': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '130', 'null': 'True'}),
            'zbroja': ('django.db.models.fields.IntegerField', [], {}),
            'zelazo': ('django.db.models.fields.IntegerField', [], {}),
            'zloto': ('django.db.models.fields.IntegerField', [], {})
        },
        'lpp_app.armia_osada': {
            'Meta': {'object_name': 'Armia_osada'},
            'armia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lpp_app.Armia']", 'null': 'True', 'blank': 'True'}),
            'drewno': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilosc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'kamien': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'osada': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lpp_app.Osada']", 'null': 'True', 'blank': 'True'}),
            'poziom': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'zelazo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'zloto': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'lpp_app.budynki': {
            'Meta': {'object_name': 'Budynki'},
            'drewno': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jednostka_prod': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'kamien': ('django.db.models.fields.IntegerField', [], {}),
            'koszt': ('django.db.models.fields.IntegerField', [], {}),
            'max_pojemnosc': ('django.db.models.fields.IntegerField', [], {}),
            'max_poziom': ('django.db.models.fields.IntegerField', [], {}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'produktywnosc': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '130', 'null': 'True'}),
            'zelazo': ('django.db.models.fields.IntegerField', [], {}),
            'zloto': ('django.db.models.fields.IntegerField', [], {})
        },
        'lpp_app.budynki_osada': {
            'Meta': {'object_name': 'Budynki_osada'},
            'budynek': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lpp_app.Budynki']", 'null': 'True', 'blank': 'True'}),
            'drewno': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilosc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'kamien': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'max_pojemnosc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'osada': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lpp_app.Osada']", 'null': 'True', 'blank': 'True'}),
            'poziom': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'produkcja': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'produktywnosc': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'zelazo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'zloto': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        'lpp_app.friends': {
            'Meta': {'object_name': 'Friends'},
            'has_friends': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'is_friend_of'", 'symmetrical': 'False', 'to': "orm['lpp_app.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'lpp_app.invites': {
            'Meta': {'unique_together': "(('user_from', 'user_to'),)", 'object_name': 'Invites'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invites'", 'to': "orm['lpp_app.UserProfile']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invited'", 'to': "orm['lpp_app.UserProfile']"})
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
            'Meta': {'unique_together': "(('nazwa',),)", 'object_name': 'Osada'},
            'data_powstania': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'drewno': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kamien': ('django.db.models.fields.IntegerField', [], {'default': '300'}),
            'nazwa': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'rozwoj': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lpp_app.UserProfile']", 'unique': 'True'}),
            'zelazo': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'zloto': ('django.db.models.fields.IntegerField', [], {'default': '10', 'null': 'True'})
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