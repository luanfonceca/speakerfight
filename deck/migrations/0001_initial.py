# Generated by Django 2.2.7 on 2019-11-20 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jury', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=200, overwrite=True, populate_from='title', unique=True)),
                ('description', models.TextField(blank=True, max_length=10000, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish')),
                ('start_timetable', models.TimeField(null=True, verbose_name='Start Timetable')),
                ('end_timetable', models.TimeField(null=True, verbose_name='End Timetable')),
                ('track_order', models.SmallIntegerField(blank=True, null=True, verbose_name='Order')),
                ('activity_type', models.CharField(choices=[('proposal', 'Proposal'), ('workshop', 'Workshop'), ('openning', 'Openning'), ('coffee-break', 'Coffee Break'), ('lunch', 'Lunch'), ('lightning-talks', 'Lightning Talks'), ('ending', 'Ending')], default='proposal', max_length=50, verbose_name='Type')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activitys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
                'ordering': ('track_order', 'start_timetable', 'pk'),
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=200, overwrite=True, populate_from='title', unique=True)),
                ('description', models.TextField(blank=True, max_length=10000, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish')),
                ('allow_public_voting', models.BooleanField(default=True, verbose_name='Allow Public Voting')),
                ('closing_date', models.DateTimeField()),
                ('slots', models.SmallIntegerField(default=10, verbose_name='Slots')),
                ('anonymous_voting', models.BooleanField(default=False, verbose_name='Anonymous Voting?')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
                ('jury', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='jury.Jury')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['-closing_date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('activity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='deck.Activity')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is approved')),
                ('more_information', models.TextField(blank=True, max_length=10000, null=True, verbose_name='More information')),
                ('slides_url', models.CharField(blank=True, max_length=250, null=True, verbose_name='speakerdeck.com/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposals', to='deck.Event')),
            ],
            options={
                'verbose_name': 'Proposal',
                'verbose_name_plural': 'Proposals',
                'ordering': ['title'],
            },
            bases=('deck.activity',),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=200, overwrite=True, populate_from='title', unique=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='deck.Event')),
            ],
            options={
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='deck.Track'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.SmallIntegerField(blank=True, choices=[(-1, 'angry'), (1, 'sad'), (0, 'sleepy'), (2, 'happy'), (3, 'laughing')], null=True, verbose_name='Rate Index')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='deck.Proposal')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
                'unique_together': {('proposal', 'user')},
            },
        ),
    ]
