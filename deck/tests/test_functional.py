from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from deck.models import Event, Proposal, Vote
from deck.tests.test_unit import EVENT_DATA, PROPOSAL_DATA


class EventTest(TestCase):
    fixtures = ['socialapp.json', 'user.json']

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


class ProposalTest(TestCase):
    fixtures = ['socialapp.json', 'user.json']

    def setUp(self):
        self.client = Client()
        self.event = Event.objects.create(**EVENT_DATA)
        self.proposal_data = PROPOSAL_DATA.copy()
        self.proposal_data.update(event=self.event)
        self.proposal = Proposal.objects.create(**self.proposal_data)
        self.client.login(username='user', password='user')

    def test_update_proposal(self):
        new_proposal_data = self.proposal_data.copy()
        new_proposal_data['description'] = 'A really really good proposal.'

        self.assertEquals(self.proposal_data['description'],
                          self.proposal.description)
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

    def test_rate_proposal(self):
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
        self.assertEquals(3, self.proposal.rate)

    def test_rate_proposal_in_a_disallowed_event(self):
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
        self.assertEquals(0, self.proposal.rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_overrated_value(self):
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
        self.assertEquals(0, self.proposal.rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())

    def test_rate_proposal_multiple_times(self):
        rate_proposal_data = {
            'event_slug': self.proposal.event.slug,
            'slug': self.proposal.slug,
            'rate': 'laughing'
        }
        self.client.get(reverse('rate_proposal', kwargs=rate_proposal_data),
                        follow=True)

        rate_proposal_data.update({'rate': 'happy'})
        response = self.client.get(
            reverse('rate_proposal', kwargs=rate_proposal_data),
            follow=True
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Vote.objects.count())
        self.assertEquals(1, self.proposal.votes.count())
        self.assertEquals(3, self.proposal.rate)

    def test_rate_proposal_with_the_same_author(self):
        self.client.login(username='admin', password='admin')

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
        self.assertEquals(0, self.proposal.rate)
        self.assertEquals(0, self.proposal.votes.count())
        self.assertEquals(0, Vote.objects.count())
