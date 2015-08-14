# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jury', '0002_auto_20150728_1433'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jury',
            options={'verbose_name': 'Jury', 'verbose_name_plural': 'Juries'},
        ),
    ]
