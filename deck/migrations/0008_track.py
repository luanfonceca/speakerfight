# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


def create_tracks(apps, schema_editor):
    Event = apps.get_model("deck", "Event")
    Track = apps.get_model("deck", "Track")

    for event in Event.objects.all():
        Track.objects.create(event=event)


def reverse_create_tracks(apps, schema_editor):
    Event = apps.get_model("deck", "Event")

    for event in Event.objects.all():
        event.tracks.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0007_event_slots'),
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
        migrations.RunPython(code=create_tracks,
                             reverse_code=reverse_create_tracks),
    ]
