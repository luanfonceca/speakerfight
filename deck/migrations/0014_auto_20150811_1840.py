# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0013_auto_20150811_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='track',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='track_order',
        ),
        migrations.AlterField(
            model_name='activity',
            name='timetable',
            field=models.TimeField(default=datetime.datetime(2015, 8, 11, 21, 40, 11, 91012, tzinfo=utc), verbose_name='Timetable'),
            preserve_default=True,
        ),
    ]
