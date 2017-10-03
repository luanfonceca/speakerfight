from mock import Mock, call

from django.test import TestCase

from deck.models import Proposal, Track, Event
from deck.use_cases import initialize_event_schedule


class InitializeEventScheduleTestCase(TestCase):

    def test_initialize_event_schedule_with_top_approved_proposals(self):
        not_scheduled_proposals = [Mock(Proposal), Mock(Proposal)]
        track = Mock(Track)
        track.has_activities.return_value = False
        event = Mock(Event)
        event.get_main_track.return_value = track
        event.filter_not_scheduled_by_slots.return_value = not_scheduled_proposals

        executed = initialize_event_schedule(event)
        self.assertTrue(executed)

        event.get_main_track.assert_called_once_with()
        track.has_activities.assert_called_once_with()
        event.filter_not_scheduled_by_slots.assert_called_once_with()
        track.add_proposal_to_slot.assert_has_calls([
            call(not_scheduled_proposals[0], 0),
            call(not_scheduled_proposals[1], 1),
        ])
