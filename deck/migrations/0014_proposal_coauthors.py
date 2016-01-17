# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deck', '0013_proposal_more_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='coauthors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
