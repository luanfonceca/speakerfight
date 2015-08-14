# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import django_extensions.db.fields
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deck', '0011_auto_20150729_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=200, blank=True, unique=True, overwrite=True)),
                ('description', models.TextField(max_length=10000, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish')),
                ('timetable', models.TimeField(default=datetime.datetime(2015, 8, 11, 21, 32, 36, 785789, tzinfo=utc), verbose_name='Timetable')),
                ('track_order', models.SmallIntegerField(null=True, verbose_name='Order', blank=True)),
                ('activity_type', models.CharField(default=b'proposal', choices=[('Proposal', b'proposal'), ('Openning', b'openning'), ('Coffee Break', b'coffee-break'), ('Lunch', b'lunch'), ('Lightning Talks', b'lightning-talks'), ('Ending', b'ending')], max_length=50, blank=True, null=True, verbose_name='Type')),
                ('author', models.ForeignKey(related_name='activitys', to=settings.AUTH_USER_MODEL)),
                ('track', models.ForeignKey(related_name='activities', blank=True, to='deck.Track', null=True)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
    ]
