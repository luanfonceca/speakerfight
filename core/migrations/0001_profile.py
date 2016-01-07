# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('core', 'Profile')
    db_alias = schema_editor.connection.alias
    for user in User.objects.using(db_alias).all():
        Profile.objects.create(user=user)


def delete_profiles(apps, schema_editor):
    Profile = apps.get_model('core', 'Profile')
    db_alias = schema_editor.connection.alias
    Profile.objects.using(db_alias).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about_me', models.TextField(max_length=500, null=True, verbose_name='About me', blank=True)),
                ('github', models.CharField(max_length=50, null=True, verbose_name='Github username', blank=True)),
                ('facebook', models.CharField(max_length=50, null=True, verbose_name='Facebook username', blank=True)),
                ('site', models.URLField(null=True, verbose_name='Site url', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(create_profiles, delete_profiles),
    ]
