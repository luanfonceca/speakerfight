# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0009_auto_20150728_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='track_order',
            field=models.SmallIntegerField(null=True, verbose_name='Order', blank=True),
            preserve_default=True,
        ),
    ]
