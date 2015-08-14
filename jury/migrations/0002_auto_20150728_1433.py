# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jury', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jury',
            options={'verbose_name': 'Juri', 'verbose_name_plural': 'j\xfaris'},
        ),
    ]
