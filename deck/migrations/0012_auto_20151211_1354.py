# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0011_auto_20150825_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(default=b'proposal', max_length=50, verbose_name='Type', choices=[(b'proposal', 'Proposal'), (b'workshop', 'Workshop'), (b'openning', 'Openning'), (b'coffee-break', 'Coffee Break'), (b'lunch', 'Lunch'), (b'lightning-talks', 'Lightning Talks'), (b'ending', 'Ending')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='activity_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='deck.Activity'),
            preserve_default=True,
        ),
    ]
