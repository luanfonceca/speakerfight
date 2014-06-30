# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Removing data 'twitter' from the SocialApp Model"
        try:
            SocialApp = orm['allauth.SocialApp']
        except KeyError:
            from allauth.socialaccount.models import SocialApp
        try:
            provider = SocialApp.objects.get(provider='twitter')
        except SocialApp.DoesNotExist:
            pass
        else:
            provider.delete()

    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("Cannot reverse this migration.")

    models = {

    }

    complete_apps = ['allauth', 'core']
    symmetrical = True
