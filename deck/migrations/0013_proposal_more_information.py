# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0012_auto_20151211_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='more_information',
            field=models.TextField(max_length=10000, null=True, verbose_name='More information', blank=True),
            preserve_default=True,
        ),
    ]
