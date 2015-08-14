# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


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
        ('deck', '0008_auto_20150728_1948'),
    ]

    operations = [
        migrations.RunPython(code=create_tracks,
                             reverse_code=reverse_create_tracks),
    ]
