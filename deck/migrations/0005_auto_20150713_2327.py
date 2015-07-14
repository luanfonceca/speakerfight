# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0004_auto_20150601_2200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposal',
            options={'ordering': ['title'], 'verbose_name': 'Proposal', 'verbose_name_plural': 'Proposals'},
        ),
    ]
