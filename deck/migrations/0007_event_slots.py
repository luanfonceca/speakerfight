# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0006_proposal_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slots',
            field=models.SmallIntegerField(default=10, verbose_name='Slots'),
            preserve_default=True,
        ),
    ]
