from model_mommy import mommy
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from deck.models import Vote


class CreateEventScheduleViewTests(TestCase):

    def setUp(self):
        # DB Setup
        tomorrow = timezone.now() + timedelta(days=1)
        self.event = mommy.make('deck.Event', _fill_optional=['jury'], slots=3, due_date=tomorrow)
        proposals = mommy.make('deck.Proposal', event=self.event, is_approved=False, _quantity=5)
        approved_proposals = [
            mommy.make(Vote, proposal=proposals[0], rate=Vote.LAUGHING),
            mommy.make(Vote, proposal=proposals[1], rate=Vote.HAPPY),
            mommy.make(Vote, proposal=proposals[2], rate=Vote.SAD),
        ]
        not_approved_proposals = [
            mommy.make(Vote, proposal=proposals[3], rate=Vote.SLEEPY),
            mommy.make(Vote, proposal=proposals[4], rate=Vote.ANGRY),
        ]

        self.url = reverse('create_event_schedule', args=[self.event.slug])

    def test_renders_correct_template_if_user_belongs_to_jury(self):
        # Request Setup
        user = mommy.make(settings.AUTH_USER_MODEL)
        self.event.jury.users.add(user)
        self.client.force_login(user)

        # HTTP Request
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'event/event_create_schedule.html')

    def test_redirect_to_view_event_if_user_does_not_belong_to_jury(self):
        # Request Setup
        user = mommy.make(settings.AUTH_USER_MODEL)
        self.client.force_login(user)

        # HTTP Request
        response = self.client.get(self.url)
        redirect_url = reverse('view_event', args=[self.event.slug])

        self.assertRedirects(response, redirect_url)

    def test_renders_correct_template_if_superuser(self):
        # Request Setup
        user = mommy.make(settings.AUTH_USER_MODEL, is_superuser=True)
        self.client.force_login(user)

        # HTTP Request
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'event/event_create_schedule.html')
