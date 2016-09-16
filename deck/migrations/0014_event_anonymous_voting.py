# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0013_proposal_more_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='anonymous_voting',
            field=models.BooleanField(default=False, verbose_name='Anonymous Voting?'),
            preserve_default=True,
        ),
    ]
