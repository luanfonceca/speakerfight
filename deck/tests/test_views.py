from model_mommy import mommy
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from deck.models import Vote


class CreateEventScheduleViewTests(TestCase):

    def test_renders_correct_template_if_user_belongs_to_jury(self):
        # DB Setup
        tomorrow = timezone.now() + timedelta(days=1)
        event = mommy.make('deck.Event', _fill_optional=['jury'], slots=3, due_date=tomorrow)
        proposals = mommy.make('deck.Proposal', event=event, is_approved=False, _quantity=5)
        approved_proposals = [
            mommy.make(Vote, proposal=proposals[0], rate=Vote.LAUGHING),
            mommy.make(Vote, proposal=proposals[1], rate=Vote.HAPPY),
            mommy.make(Vote, proposal=proposals[2], rate=Vote.SAD),
        ]
        not_approved_proposals = [
            mommy.make(Vote, proposal=proposals[3], rate=Vote.SLEEPY),
            mommy.make(Vote, proposal=proposals[4], rate=Vote.ANGRY),
        ]

        # Request Setup
        user = mommy.make(settings.AUTH_USER_MODEL)
        event.jury.users.add(user)
        self.client.force_login(user)
        url = reverse('create_event_schedule', args=[event.slug])

        # HTTP Request
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'event/event_create_schedule.html')
