# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0002_auto_20150405_1831'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-due_date', '-created_at'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vote',
            name='rate',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Rate Index', choices=[(-1, b'angry'), (1, b'sad'), (0, b'sleepy'), (2, b'happy'), (3, b'laughing')]),
            preserve_default=True,
        ),
    ]
