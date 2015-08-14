# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from datetime import datetime, date, timedelta
import datetime

from django.db import models, migrations
from django.utils.timezone import utc


def add_to_time(value, minutes):
    today = datetime.date.today()
    full_datetime = datetime.datetime.combine(today, value)
    added_datetime = full_datetime + datetime.timedelta(minutes=minutes)
    return added_datetime.time()


def update_start_and_end_timetables(apps, schema_editor):
    Activity = apps.get_model("deck", "Activity")

    for activity in Activity.objects.all():
        activity.end_timetable = add_to_time(activity.timetable, minutes=30)
        activity.start_timetable = activity.timetable
        activity.save()


def reserve_update_start_and_end_timetables(apps, schema_editor):
    Activity = apps.get_model("deck", "Activity")

    Activity.objects.update(timetable=models.F('start_timetable'))


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0016_auto_20150811_1847'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ('track_order', 'start_timetable', 'pk'), 'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
        migrations.AddField(
            model_name='activity',
            name='end_timetable',
            field=models.TimeField(default=datetime.datetime(2015, 8, 14, 19, 36, 25, 450039, tzinfo=utc), null=True, verbose_name='End Timetable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='start_timetable',
            field=models.TimeField(default=datetime.datetime(2015, 8, 14, 19, 36, 25, 449986, tzinfo=utc), null=True, verbose_name='Start Timetable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(default=b'proposal', max_length=50, verbose_name='Type', choices=[(b'proposal', 'Proposal'), (b'openning', 'Openning'), (b'coffee-break', 'Coffee Break'), (b'lunch', 'Lunch'), (b'lightning-talks', 'Lightning Talks'), (b'ending', 'Ending')]),
            preserve_default=True,
        ),
        migrations.RunPython(
            code=update_start_and_end_timetables,
            reverse_code=reserve_update_start_and_end_timetables
        ),
        migrations.RemoveField(
            model_name='activity',
            name='timetable',
        ),
    ]
