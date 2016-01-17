# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0014_proposal_coauthors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='coauthors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
    ]
