# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0010_proposal_track_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='track_order',
            field=models.SmallIntegerField(default=None, null=True, verbose_name='Order', blank=True),
            preserve_default=True,
        ),
    ]
