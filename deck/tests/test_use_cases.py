from mock import Mock, call

from django.test import TestCase

from deck.models import Proposal, Track, Event, Activity
from deck.use_cases import initialize_event_schedule, rearrange_event_schedule


class InitializeEventScheduleTestCase(TestCase):

    def setUp(self):
        self.track = Mock(Track)
        self.event = Mock(Event)
        self.event.get_main_track.return_value = self.track

    def test_initialize_event_schedule_with_top_approved_proposals(self):
        self.track.has_activities.return_value = False
        not_scheduled_proposals = [Mock(Proposal), Mock(Proposal)]
        self.event.filter_not_scheduled_by_slots.return_value = not_scheduled_proposals

        executed = initialize_event_schedule(self.event)
        self.assertTrue(executed)

        self.event.get_main_track.assert_called_once_with()
        self.track.has_activities.assert_called_once_with()
        self.event.filter_not_scheduled_by_slots.assert_called_once_with()
        self.track.add_proposal_to_slot.assert_has_calls([
            call(not_scheduled_proposals[0], 0),
            call(not_scheduled_proposals[1], 1),
        ])

    def test_do_not_initialize_event_schedule_if_main_track_already_has_activities(self):
        self.track.has_activities.return_value = True

        executed = initialize_event_schedule(self.event)
        self.assertTrue(executed)

        self.event.get_main_track.assert_called_once_with()
        self.track.has_activities.assert_called_once_with()
        self.assertFalse(self.event.filter_not_scheduled_by_slots.called)
        self.assertFalse(self.track.add_proposal_to_slot.called)


class RearrangeEventScheduleTestCase(TestCase):

    def setUp(self):
        self.track = Mock(Track)
        self.event = Mock(Event)
        self.event.get_main_track.return_value = self.track

    def test_rearrange_event_schedule_respecting_new_activitites_arrangement(self):
        activities = [Mock(Activity), Mock(Activity)]

        returned_activities = rearrange_event_schedule(self.event, activities)

        self.assertEqual(activities, returned_activities)
        self.event.get_main_track.assert_called_once_with()
        self.track.refresh_track.assert_called_once_with()
        self.track.add_activity_to_slot.assert_has_calls([
            call(activities[0], 0),
            call(activities[1], 1),
        ])
