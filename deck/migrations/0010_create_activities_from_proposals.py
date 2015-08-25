# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_activities(apps, schema_editor):
    Proposal = apps.get_model("deck", "Proposal")
    Activity = apps.get_model("deck", "Activity")

    for proposal in Proposal.objects.all():
        Activity.objects.create(
            pk=proposal.pk,
            title=proposal.title,
            slug=proposal.slug,
            description=proposal.description,
            created_at=proposal.created_at,
            is_published=proposal.is_published,
            activity_type='proposal',
            author=proposal.author,
        )


def reverse_create_activities(apps, schema_editor):
    Event = apps.get_model("deck", "Event")

    for event in Event.objects.all():
        event.tracks.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('deck', '0009_activity'),
    ]

    operations = [
        migrations.RunPython(
            code=create_activities,
            reverse_code=reverse_create_activities),
    ]
