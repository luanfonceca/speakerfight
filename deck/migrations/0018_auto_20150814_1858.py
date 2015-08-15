# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0017_auto_20150814_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='end_timetable',
            field=models.TimeField(null=True, verbose_name='End Timetable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_timetable',
            field=models.TimeField(null=True, verbose_name='Start Timetable'),
            preserve_default=True,
        ),
    ]
