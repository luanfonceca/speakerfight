# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0010_create_activities_from_proposals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='author',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='description',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='id',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='title',
        ),
        migrations.AddField(
            model_name='proposal',
            name='activity_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=None, serialize=False, to='deck.Activity'),
            preserve_default=False,
        ),
    ]
