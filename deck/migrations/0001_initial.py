# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jury', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=60, blank=True, unique=True, overwrite=True)),
                ('description', models.TextField(max_length=400, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('is_published', models.BooleanField(default=False, verbose_name='Publish')),
                ('allow_public_voting', models.BooleanField(default=True, verbose_name='Allow Public Voting')),
                ('due_date', models.DateTimeField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name='events', to=settings.AUTH_USER_MODEL)),
                ('jury', models.OneToOneField(related_name='event', null=True, blank=True, to='jury.Jury')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'title', max_length=60, blank=True, unique=True, overwrite=True)),
                ('description', models.TextField(max_length=400, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('is_published', models.BooleanField(default=False, verbose_name='Publish')),
                ('author', models.ForeignKey(related_name='proposals', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(related_name='proposals', to='deck.Event')),
            ],
            options={
                'verbose_name': 'Proposal',
                'verbose_name_plural': 'Proposals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.SmallIntegerField(blank=True, null=True, verbose_name='Rate Index', choices=[(-1, b'angry'), (0, b'sleepy'), (1, b'sad'), (2, b'happy'), (3, b'laughing')])),
                ('proposal', models.ForeignKey(related_name='votes', to='deck.Proposal')),
                ('user', models.ForeignKey(related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('proposal', 'user')]),
        ),
    ]
