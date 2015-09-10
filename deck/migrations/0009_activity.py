# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deck', '0008_track'),
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
                ('start_timetable', models.TimeField(null=True, verbose_name='Start Timetable')),
                ('end_timetable', models.TimeField(null=True, verbose_name='End Timetable')),
                ('track_order', models.SmallIntegerField(null=True, verbose_name='Order', blank=True)),
                ('activity_type', models.CharField(default=b'proposal', max_length=50, verbose_name='Type', choices=[(b'proposal', 'Proposal'), (b'openning', 'Openning'), (b'coffee-break', 'Coffee Break'), (b'lunch', 'Lunch'), (b'lightning-talks', 'Lightning Talks'), (b'ending', 'Ending')])),
                ('author', models.ForeignKey(related_name='activitys', to=settings.AUTH_USER_MODEL)),
                ('track', models.ForeignKey(related_name='activities', blank=True, to='deck.Track', null=True)),
            ],
            options={
                'ordering': ('track_order', 'start_timetable', 'pk'),
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
    ]
