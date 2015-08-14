# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.models.signals import post_save
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0007_auto_20150728_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=200, blank=True, unique=True, overwrite=True)),
                ('event', models.ForeignKey(related_name='tracks', to='deck.Event')),
            ],
            options={
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='event',
            name='tracks',
        ),
        migrations.AddField(
            model_name='event',
            name='is_grade_published',
            field=models.BooleanField(default=False, verbose_name='Publish grade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='track',
            field=models.ForeignKey(related_name='proposals', blank=True, to='deck.Track', null=True),
            preserve_default=True,
        ),
    ]
