# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0003_auto_20150531_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Publish'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Publish'),
            preserve_default=True,
        ),
    ]
