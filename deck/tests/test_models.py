from datetime import timedelta
from mock import patch
from model_mommy import mommy

from django.test import TestCase
from django.utils import timezone

from deck.models import Event, Track, Proposal


class EventModelTests(TestCase):

    def setUp(self):
        tomorrow = timezone.now() + timedelta(days=1)
        self.event = mommy.make(Event, slots=3, due_date=tomorrow)

    def test_get_main_track_returns_first_track(self):
        # first track is created automagically via post-save
        existing_track = Track.objects.get(event=self.event)
        extra_track = mommy.make(Track, event=self.event)

        main_track = self.event.get_main_track()

        self.assertEqual(existing_track, main_track)

    @patch.object(Event, 'get_not_approved_schedule')
    def test_filter_not_scheduled_by_slots(self, mocked_get_not_approved_schedule):
        mommy.make(Proposal, event=self.event, _quantity=5)
        event_proposals = Proposal.objects.filter(event=self.event)
        mocked_get_not_approved_schedule.return_value = event_proposals

        to_schedule_proposals = self.event.filter_not_scheduled_by_slots()

        self.assertEqual(3, len(to_schedule_proposals))
        for proposal in event_proposals[:3]:
            self.assertIn(proposal, to_schedule_proposals)
