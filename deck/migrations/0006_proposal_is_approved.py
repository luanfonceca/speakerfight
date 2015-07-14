# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0005_auto_20150713_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Is approved'),
            preserve_default=True,
        ),
    ]
