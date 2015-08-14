# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0015_auto_20150811_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='timetable',
            field=models.TimeField(default=datetime.datetime(2015, 8, 11, 21, 47, 15, 197611, tzinfo=utc), null=True, verbose_name='Timetable', blank=True),
            preserve_default=True,
        ),
    ]
