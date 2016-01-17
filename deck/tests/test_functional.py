from collections import namedtuple
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from datetime import datetime, timedelta

from deck.models import (Event, Proposal, Vote, Jury,
                         send_proposal_deleted_mail, send_welcome_mail)
from deck.tests.test_unit import (
    EVENT_DATA, PROPOSAL_DATA, ANOTHER_PROPOSAL_DATA)


class EventTest(TestCase):
    fixtures = ['user.json', 'socialapp.json']

    def setUp(self):
        self.client = Client()
        self.event_data = EVENT_DATA.copy()
        self.proposal_data = PROPOSAL_DATA.copy()
        self.client.login(username='admin', password='admin')

    def test_create_event(self):
        response = self.client.post(reverse('create_event'),
                                    self.event_data, follow=True)
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(Event.objects.all(),
                                 ["<Event: RuPy>"])
        self.assertQuerysetEqual(response.context['request'].user.events.all(),
                                 ["<Event: RuPy>"])

        event = response.context['event']
        self.assertEquals('RuPy', event.title)
        self.assertEquals('A really good event.', event.description)
        self.assertEquals('admin', event.author.username)
        self.assertEquals(False, event.is_published)

    def test_notify_event_creator_after_creation(self):
        if not settings.SEND_NOTIFICATIONS:
            return

        self.client.post(reverse('create_event'), self.event_data)
        event = Event.objects.get()

        self.assertEqual(1, len(mail.outbox))
        email = mail.outbox[0]
        self.assertIn(event.author.email, email.recipients())
        self.assertIn(settings.NO_REPLY_EMAIL, email.from_email)

    def test_create_event_with_jury(self):
        event_data = self.event_data.copy()

        response = self.client.post(reverse('create_event'),
                                    event_data, follow=True)
        self.assertEquals(200, response.status_code)

        event = response.context['event']
        self.assertEquals(Jury.objects.count(), 1)
        self.assertQuerysetEqual(event.jury.users.all(), ['<User: admin>'])

    def test_anonymous_user_create_events(self):
        self.client.logout()
        response = self.client.post(reverse('create_event'),
                                    self.event_data, follow=True)
        self.assertEquals(200, response.status_code)
        self.assertEquals(reverse('create_event'),
                          response.context_data.get('redirect_field_value'))
        self.assertEquals(0, Event.objects.count())

    def test_empty_list_event(self):
        self.client.login(username='user', password='user')

        Event.objects.create(**self.event_data)
        response = self.client.get(reverse('list_events'), follow=True)
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_list'], [])

    def test_list_event(self):
        event_data = self.event_data.copy()
        event_data.update(is_published=True)
        Event.objects.create(**event_data)

        response = self.client.get(reverse('list_events'), follow=True)
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_list'],
                                 ["<Event: RuPy>"])

    def test_detail_event(self):
        event = Event.objects.create(**self.event_data)
        response = self.client.get(
            reverse('view_event', kwargs={'slug': event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)

        event = response.context['event']
        self.assertEquals('RuPy', event.title)
        self.assertEquals('A really good event.', event.description)

    def test_detail_from_an_event_with_now_allow_public_voting(self):
        self.client.logout()
        event_data = self.event_data.copy()
        event_data.update(allow_public_voting=False)
        event = Event.objects.create(**event_data)
        response = self.client.get(
            reverse('view_event', kwargs={'slug': event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual([], response.context['event_proposals'])

    def test_update_event(self):
        event = Event.objects.create(**self.event_data)
        self.assertEquals(1, Event.objects.count())

        new_event_data = self.event_data.copy()
        new_event_data['description'] = 'A really really good event.'

        self.assertEquals(self.event_data['description'], event.description)
        response = self.client.post(reverse('update_event',
                                            kwargs={'slug': event.slug}),
                                    new_event_data, follow=True)

        self.assertEquals(200, response.status_code)
        event = response.context['event']
        self.assertEquals('RuPy', event.title)
        self.assertEquals('A really really good event.',
                          event.description)

    def test_update_event_title(self):
        event = Event.objects.create(**self.event_data)
        new_event_data = self.event_data.copy()
        new_event_data['title'] = 'RuPy 2014'

        self.assertEquals(self.event_data['title'], event.title)
        response = self.client.post(
            reverse('update_event', kwargs={'slug': event.slug}),
            new_event_data, follow=True
        )

        self.assertEquals(200, response.status_code)
        event = response.context['event']
        self.assertEquals('rupy-2014', event.slug)

    def test_anonymous_user_update_events(self):
        self.client.logout()
        event = Event.objects.create(**self.event_data)
        event_update_url = reverse('update_event',
                                   kwargs={'slug': event.slug})
        new_event_data = self.event_data.copy()
        new_event_data['title'] = 'RuPy 2014'
        response = self.client.post(
            event_update_url,
            new_event_data, follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(event_update_url,
                          response.context_data.get('redirect_field_value'))
        self.assertEquals('RuPy', event.title)

    def test_not_author_update_events(self):
        self.client.login(username='user', password='user')
        event = Event.objects.create(**self.event_data)
        event_update_url = reverse('update_event',
                                   kwargs={'slug': event.slug})
        new_event_data = self.event_data.copy()
        new_event_data['title'] = 'RuPy 2014'
        response = self.client.post(
            event_update_url,
            new_event_data, follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals('event/event_detail.html', response.template_name[0])
        self.assertEquals('RuPy', event.title)

    def test_publish_event(self):
        event = Event.objects.create(**self.event_data)
        event_data = self.event_data.copy()
        event_data['is_published'] = True

        self.assertEquals(False, event.is_published)
        response = self.client.post(
            reverse('update_event', kwargs={'slug': event.slug}),
            event_data, follow=True
        )

        self.assertEquals(200, response.status_code)
        event = response.context['event']
        self.assertEquals(True, event.is_published)

    def test_event_create_event_proposal_context(self):
        event = Event.objects.create(**self.event_data)
        response = self.client.get(
            reverse('create_event_proposal', kwargs={'slug': event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(event, response.context['event'])

    def test_event_create_event_proposal(self):
        event = Event.objects.create(**self.event_data)
        response = self.client.post(
            reverse('create_event_proposal', kwargs={'slug': event.slug}),
            self.proposal_data, follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(Proposal.objects.all(),
                                 ["<Proposal: Python For Zombies>"])
        self.assertQuerysetEqual(event.proposals.all(),
                                 ["<Proposal: Python For Zombies>"])

        python_for_zombies = event.proposals.get()
        self.assertEquals('Python For Zombies', python_for_zombies.title)
        self.assertEquals('Brain...', python_for_zombies.description)

    def test_event_create_event_proposal_with_coauthor(self):
        event = Event.objects.create(**self.event_data)
        coauthor = {"coauthors": 2}
        self.proposal_data.update(coauthor)
        response = self.client.post(
            reverse('create_event_proposal', kwargs={'slug': event.slug}),
            self.proposal_data, follow=True
        )
        self.assertEquals(200, response.status_code)
        proposal = event.proposals.get()
        self.assertIn(User.objects.get(id=2), proposal.coauthors.all())

    def test_notify_event_jury_and_proposal_author_on_new_proposal(self):
        if not settings.SEND_NOTIFICATIONS:
            return

        event = Event.objects.create(**self.event_data)
        self.client.post(
            reverse('create_event_proposal', kwargs={'slug': event.slug}),
            self.proposal_data, follow=True
        )
        proposal = event.proposals.get()

        self.assertEqual(2, len(mail.outbox))
        jury_email = mail.outbox[0]
        for jury in event.jury.users.all():
            self.assertIn(jury.email, jury_email.recipients())
        self.assertIn(settings.NO_REPLY_EMAIL, jury_email.from_email)

        author_email = mail.outbox[0]
        self.assertIn(proposal.author.email, author_email.recipients())
        self.assertIn(settings.NO_REPLY_EMAIL, author_email.from_email)

    def test_notify_proposal_author_and_coauthors_on_new_proposal(self):
        event = Event.objects.create(**self.event_data)
        coauthor = {"coauthors": 2}
        self.proposal_data.update(coauthor)
        self.client.post(
            reverse('create_event_proposal', kwargs={'slug': event.slug}),
            self.proposal_data, follow=True
        )
        proposal = event.proposals.get()

        authors_emails = mail.outbox[1]
        coauthor_email = User.objects.get(id=2)
        self.assertIn(proposal.author.email, authors_emails.recipients())
        self.assertIn(coauthor_email.email, authors_emails.recipients())

    def test_anonymous_user_create_event_proposal(self):
        event = Event.objects.create(**self.event_data)
        self.client.logout()
        event_create_proposal_url = reverse(
            'create_event_proposal', kwargs={'slug': event.slug})
        response = self.client.post(
            event_create_proposal_url,
            self.proposal_data, follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(event_create_proposal_url,
                          response.context_data.get('redirect_field_value'))
        self.assertEquals(0, event.proposals.count())

    def test_event_create_event_proposal_with_passed_due_date(self):
        event_data = self.event_data.copy()
        event_data.update(due_date=datetime.now() - timedelta(hours=24))
        event = Event.objects.create(**event_data)
        with self.assertRaises(ValidationError):
            self.client.post(
                reverse('create_event_proposal', kwargs={'slug': event.slug}),
                self.proposal_data
            )
        self.assertEquals(0, event.proposals.count())

        response = self.client.get(
            reverse('create_event_proposal', kwargs={'slug': event.slug}))
        self.assertEqual(302, response.status_code)

    def test_export_votes_to_csv_queryset(self):
        event = Event.objects.create(**self.event_data)
        Proposal.objects.create(event=event, **self.proposal_data)
        proposals = event.get_votes_to_export()
        exported_data = [{'title': u'Python For Zombies',
                          'votes__count': 0,
                          'author__email': u'admin@speakerfight.com',
                          'author__username': u'admin',
                          'votes__rate__sum': None,
                          'id': 1}]
        self.assertEqual(list(proposals), exported_data)

    def test_export_votes_sum_rate(self):
        event = Event.objects.create(**self.event_data)
        proposal = Proposal.objects.create(event=event, **self.proposal_data)
        user = User.objects.get(username='user')
        another_user = User.objects.get(username='another')
        Vote.objects.create(user=user, proposal=proposal, rate=2)
        Vote.objects.create(user=another_user, proposal=proposal, rate=-1)
        proposals = list(event.get_votes_to_export())
        sum_rate = sum(proposal['votes__rate__sum'] for proposal in proposals)
        self.assertEqual(1, sum_rate)

    def test_export_votes_count(self):
        event = Event.objects.create(**self.event_data)
        proposal = Proposal.objects.create(event=event, **self.proposal_data)
        user = User.objects.get(username='user')
        another_user = User.objects.get(username='another')
        Vote.objects.create(user=user, proposal=proposal, rate=1)
        Vote.objects.create(user=another_user, proposal=proposal, rate=1)
        proposals = list(event.get_votes_to_export())
        total_votes = sum(proposal['votes__count'] for proposal in proposals)
        self.assertEqual(2, total_votes)

    def test_export_event_votes_to_csv(self):
        event = Event.objects.create(**self.event_data)
        response = self.client.get(
            reverse('export_event', kwargs={'slug': event.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_not_authorized_to_export_event_votes_to_csv(self):
        self.client.login(username='user', password='user')
        event = Event.objects.create(**self.event_data)
        response = self.client.get(
            reverse('export_event', kwargs={'slug': event.slug}))
        self.assertEqual(302, response.status_code)


class ProposalTest(TestCase):
    fixtures = ['user.json', 'socialapp.json']

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(**EVENT_DATA)
        self.proposal_data = PROPOSAL_DATA.copy()
        self.proposal_data.update(event=self.event)
        self.proposal = Proposal.objects.create(**self.proposal_data)
        self.client.login(username='user', password='user')

    def test_empty_list_proposal(self):
        self.proposal.delete()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'], [])

    def test_list_proposal(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    # Starts Admin Overview
    def test_list_proposal_as_admin_user(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    def test_list_proposal_without_public_voting_as_admin_user(self):
        self.client.login(username='admin', password='admin')
        self.event.allow_public_voting = False
        self.event.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    def test_list_proposal_without_published_and_as_admin_user(self):
        self.client.login(username='admin', password='admin')
        self.event.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    def test_list_proposal_without_public_voting_and_without_published_and_as_admin_user(self):
        self.client.login(username='admin', password='admin')
        self.event.allow_public_voting = False
        self.event.save()
        self.proposal.is_published = False
        self.proposal.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])
    # Ends Admin Overview

    # Starts Author Overview
    def test_list_proposal_as_author(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.event.author = User.objects.get(username='another')
        self.event.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    def test_list_proposal_without_public_voting_as_author(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.event.author = User.objects.get(username='another')
        self.event.allow_public_voting = False
        self.event.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    def test_list_proposal_without_published_and_as_author(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.event.author = User.objects.get(username='another')
        self.event.save()
        self.proposal.is_published = False
        self.proposal.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    def test_list_proposal_without_public_voting_and_without_published_and_as_author(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.event.author = User.objects.get(username='another')
        self.event.allow_public_voting = False
        self.event.save()
        self.proposal.is_published = False
        self.proposal.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])
    # Ends Author Overview

    # Starts User Overview
    def test_list_proposal_as_user(self):
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ['<Proposal: Python For Zombies>'])

    def test_list_proposal_without_public_voting_as_user(self):
        self.event.allow_public_voting = False
        self.event.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'], [])

    def test_list_proposal_without_published_and_as_user(self):
        self.proposal.is_published = False
        self.proposal.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ['<Proposal: Python For Zombies>'])

    def test_list_proposal_without_public_voting_and_without_published_and_as_user(self):
        self.event.allow_public_voting = False
        self.event.save()
        self.proposal.is_published = False
        self.proposal.save()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'], [])
    # Ends User Overview

    def test_list_proposal_without_logged_user(self):
        self.client.logout()
        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ['<Proposal: Python For Zombies>'])

    def test_list_proposal_without_public_voting(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.event.allow_public_voting = False
        self.event.save()

        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'], [])

    def test_list_proposal_without_public_voting_and_without_logged_user(self):
        self.client.logout()
        self.event.allow_public_voting = False
        self.event.save()

        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'], [])

    def test_list_proposal_with_public_voting(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.event.allow_public_voting = True
        self.event.save()
        self.proposal.is_published = True
        self.proposal.save()

        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>"])

    def test_list_proposal_ordering_when_user_is_logged(self):
        another_proposal_data = ANOTHER_PROPOSAL_DATA.copy()
        another_proposal_data.update(event=self.event)
        another_proposal = Proposal.objects.create(**another_proposal_data)

        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: A Python 3 Metaprogramming Tutorial>",
                                  "<Proposal: Python For Zombies>"])

        rate_proposal_data = {
            'event_slug': another_proposal.event.slug,
            'slug': another_proposal.slug,
            'rate': 'laughing'
        }
        self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        response = self.client.get(
            reverse('view_event', kwargs={'slug': self.event.slug}),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['event_proposals'],
                                 ["<Proposal: Python For Zombies>",
                                  "<Proposal: A Python 3 Metaprogramming Tutorial>"])

    def test_update_proposal(self):
        new_proposal_data = self.proposal_data.copy()
        new_proposal_data['description'] = 'A really really good proposal.'

        self.assertEquals(self.proposal_data['description'],
                          self.proposal.description)

        response = self.client.get(
            reverse('update_proposal',
                    kwargs={'event_slug': self.event.slug,
                            'slug': self.proposal.slug}))
        self.assertEqual(response.context['event'], self.event)

        response = self.client.post(
            reverse('update_proposal',
                    kwargs={'event_slug': self.event.slug,
                            'slug': self.proposal.slug}),
            new_proposal_data, follow=True)

        self.assertEquals(200, response.status_code)
        self.proposal = response.context['event'].proposals.first()
        self.assertEquals('Python For Zombies', self.proposal.title)
        self.assertEquals('A really really good proposal.',
                          self.proposal.description)

    def test_anonymous_user_update_proposal(self):
        self.client.logout()
        new_proposal_data = self.proposal_data.copy()
        new_proposal_data['description'] = 'A really really good proposal.'
        proposal_update_url = reverse(
            'update_proposal',
            kwargs={'event_slug': self.event.slug,
                    'slug': self.proposal.slug})
        response = self.client.post(
            proposal_update_url,
            new_proposal_data, follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(proposal_update_url,
                          response.context_data.get('redirect_field_value'))
        self.assertEquals('Brain...', self.proposal.description)

    def test_delete_proposal(self):
        new_proposal_data = self.proposal_data.copy()
        new_proposal_data['author_id'] = User.objects.get(username='user').id
        new_proposal_data['description'] = 'A good candidate to be deleted.'
        proposal = Proposal.objects.create(**new_proposal_data)

        self.assertEqual(
            Proposal.objects.filter(slug=proposal.slug).count(), 1)

        response = self.client.post(
            reverse('delete_proposal',
                    kwargs={'event_slug': proposal.event.slug,
                            'slug': proposal.slug}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Proposal deleted.')
        self.assertEqual(
            Proposal.objects.filter(slug=proposal.slug).count(), 0)

    def test_not_allowed_to_delete_proposal(self):
        response = self.client.post(
            reverse('delete_proposal',
                    kwargs={'event_slug': self.proposal.event.slug,
                            'slug': self.proposal.slug}), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'You are not allowed to see this page.')

    def test_rate_proposal(self):
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'laughing'
        }
        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Vote.objects.count())
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(3, self.proposal.get_rate)

    def test_rate_proposal_by_get(self):
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'laughing'
        }
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Vote.objects.count())
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(3, self.proposal.get_rate)

    def test_rate_proposal_in_a_disallowed_event(self):
        self.client.logout()
        self.client.login(username='another', password='another')

        self.event.allow_public_voting = False
        self.event.save()

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(401, response.status_code)
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_in_a_disallowed_event_by_get(self):
        self.client.logout()
        self.client.login(username='another', password='another')

        self.event.allow_public_voting = False
        self.event.save()

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_overrated_value(self):
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'whatever'
        }
        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(400, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_overrated_value_by_get(self):
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'whatever'
        }
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_multiple_times(self):
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'laughing'
        }
        self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        rate_proposal_data.update({'rate': 'happy'})
        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )
        self.assertEquals(401, response.status_code)
        self.assertEquals(1, Vote.objects.count())
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(3, self.proposal.get_rate)

    def test_rate_proposal_multiple_times_by_get(self):
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'laughing'
        }
        self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        rate_proposal_data.update({'rate': 'happy'})
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Vote.objects.count())
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(3, self.proposal.get_rate)

    def test_rate_proposal_with_the_same_author(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.proposal.author = User.objects.get(username='another')
        self.proposal.save()

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(401, response.status_code)
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_with_the_same_author_by_get(self):
        self.client.logout()
        self.client.login(username='another', password='another')
        self.proposal.author = User.objects.get(username='another')
        self.proposal.save()

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_anonymous_user_rate_proposal(self):
        self.client.logout()
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }

        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )
        self.assertEquals(401, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_anonymous_user_rate_proposal_by_get(self):
        self.client.logout()
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }

        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, self.proposal.get_rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_with_the_admin_user(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')
        self.proposal.author = User.objects.get(username='admin')
        self.proposal.save()

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, self.proposal.get_rate)
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(1, Vote.objects.count())

    def test_rate_proposal_with_the_admin_user_by_get(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')
        self.proposal.author = User.objects.get(username='admin')
        self.proposal.save()

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, self.proposal.get_rate)
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(1, Vote.objects.count())

    def test_rate_proposal_with_the_jury_user(self):
        self.event.jury.users.add(User.objects.get(username='another'))
        self.client.logout()
        self.client.login(username='another', password='another')

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.post(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, self.proposal.get_rate)
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(1, Vote.objects.count())

    def test_rate_proposal_with_the_jury_user_by_get(self):
        self.event.jury.users.add(User.objects.get(username='another'))
        self.client.logout()
        self.client.login(username='another', password='another')

        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'sad'
        }
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )

        self.assertEquals(200, response.status_code)
        self.assertEquals(1, self.proposal.get_rate)
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(1, Vote.objects.count())

    def test_approve_proposal_with_the_anonymous_user(self):
        self.client.logout()
        approve_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
        }

        response = self.client.post(
            reverse('approve_proposal', kwargs=approve_proposal_data),
            follow=True
        )
        self.proposal = Proposal.objects.first()
        self.assertEquals(401, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(False, self.proposal.is_approved)

    def test_approve_proposal_with_the_admin_user(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')
        self.proposal.author = User.objects.get(username='admin')
        self.proposal.save()

        approve_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
        }
        response = self.client.post(
            reverse('approve_proposal', kwargs=approve_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(True, self.proposal.is_approved)

    def test_approve_proposal_with_the_admin_user_by_get(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')
        self.proposal.author = User.objects.get(username='admin')
        self.proposal.save()

        approve_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug
        }
        response = self.client.get(
            reverse('approve_proposal', kwargs=approve_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertEquals(True, self.proposal.is_approved)

    def test_approve_proposal_with_the_jury_user(self):
        self.event.jury.users.add(User.objects.get(username='another'))
        self.client.logout()
        self.client.login(username='another', password='another')

        approve_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug
        }
        response = self.client.post(
            reverse('approve_proposal', kwargs=approve_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(True, self.proposal.is_approved)

    def test_approve_proposal_with_the_jury_user_by_get(self):
        self.event.jury.users.add(User.objects.get(username='another'))
        self.client.logout()
        self.client.login(username='another', password='another')

        approve_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug
        }
        response = self.client.get(
            reverse('approve_proposal', kwargs=approve_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertEquals(True, self.proposal.is_approved)

    def test_disapprove_proposal_with_the_anonymous_user(self):
        self.proposal.is_approved = True
        self.proposal.save()

        self.client.logout()
        disapprove_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
        }

        response = self.client.post(
            reverse('disapprove_proposal', kwargs=disapprove_proposal_data),
            follow=True
        )
        self.proposal = Proposal.objects.first()
        self.assertEquals(401, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(True, self.proposal.is_approved)

    def test_disapprove_proposal_with_the_admin_user(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')
        self.proposal.author = User.objects.get(username='admin')
        self.proposal.is_approved = True
        self.proposal.save()

        disapprove_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
        }
        response = self.client.post(
            reverse('disapprove_proposal', kwargs=disapprove_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(False, self.proposal.is_approved)

    def test_disapprove_proposal_with_the_admin_user_by_get(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')
        self.proposal.author = User.objects.get(username='admin')
        self.proposal.is_approved = True
        self.proposal.save()

        disapprove_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug
        }
        response = self.client.get(
            reverse('disapprove_proposal', kwargs=disapprove_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertEquals(False, self.proposal.is_approved)

    def test_disapprove_proposal_with_the_jury_user(self):
        self.event.jury.users.add(User.objects.get(username='another'))
        self.client.logout()
        self.client.login(username='another', password='another')
        self.proposal.is_approved = True
        self.proposal.save()

        disapprove_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug
        }
        response = self.client.post(
            reverse('disapprove_proposal', kwargs=disapprove_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertIn('message', json.loads(response.content))
        self.assertEquals(False, self.proposal.is_approved)

    def test_disapprove_proposal_with_the_jury_user_by_get(self):
        self.event.jury.users.add(User.objects.get(username='another'))
        self.client.logout()
        self.client.login(username='another', password='another')
        self.proposal.is_approved = True
        self.proposal.save()

        disapprove_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug
        }
        response = self.client.get(
            reverse('disapprove_proposal', kwargs=disapprove_proposal_data),
            follow=True
        )

        self.proposal = Proposal.objects.first()
        self.assertEquals(200, response.status_code)
        self.assertEquals(False, self.proposal.is_approved)

    def test_send_welcome_mail(self):
        if not settings.SEND_NOTIFICATIONS:
            return

        User = namedtuple('User', 'email')
        fake_user = User('fake@mail.com')
        send_welcome_mail(None, fake_user)

        self.assertEqual(1, len(mail.outbox))
        email = mail.outbox[0]

        self.assertTrue('Welcome', email.subject)
        self.assertIn(fake_user.email, email.recipients())
        self.assertIn(settings.NO_REPLY_EMAIL, email.from_email)

    def test_send_proposal_deleted_mail(self):
        if not settings.SEND_NOTIFICATIONS:
            return

        user = User.objects.get(username='user')
        self.proposal.event.jury.users.add(user)
        send_proposal_deleted_mail(Proposal, self.proposal)
        self.assertEqual(1, len(mail.outbox))
        email = mail.outbox[0]
        self.assertEqual('Proposal from RuPy just got deleted', email.subject)
        self.assertIn('admin@speakerfight.com', email.recipients())
        self.assertIn('user@speakerfight.com', email.recipients())
        self.assertIn('Python For Zombies', email.body)
        self.assertIn(settings.NO_REPLY_EMAIL, email.from_email)

    def test_my_proposals_menu_for_authenticated_users(self):
        response = self.client.get(reverse('list_events'))
        self.assertContains(response, 'My Proposals')

    def test_my_proposals_menu_for_non_authenticated_users(self):
        self.client.logout()
        response = self.client.get(reverse('list_events'))
        self.assertNotContains(response, 'My Proposals')

    def test_users_should_see_their_proposals(self):
        user = User.objects.get(username='user')
        self.proposal.author = user
        self.proposal.save()
        response = self.client.get(reverse('my_proposals'))
        self.assertQuerysetEqual(response.context['object_list'],
                                 ['<Proposal: Python For Zombies>'])
