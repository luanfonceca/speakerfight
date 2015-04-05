# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=200, blank=True, unique=True, overwrite=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=200, blank=True, unique=True, overwrite=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
            preserve_default=True,
        ),
    ]
