# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0014_auto_20150811_1840'),
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
        migrations.AlterField(
            model_name='activity',
            name='timetable',
            field=models.TimeField(default=datetime.datetime(2015, 8, 11, 21, 41, 12, 401257, tzinfo=utc), verbose_name='Timetable'),
            preserve_default=True,
        ),
    ]
