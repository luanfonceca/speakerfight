from datetime import timedelta
from mock import patch, Mock
from model_mommy import mommy

from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from deck.models import Event, Track, Proposal, Activity, get_activities_by_parameters_order


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

    def test_check_if_user_is_in_jury(self):
        user = mommy.make(settings.AUTH_USER_MODEL)
        self.assertFalse(self.event.user_in_jury(user))
        self.event.jury.users.add(user)
        self.assertTrue(self.event.user_in_jury(user))


class TrackModelTests(TestCase):

    def setUp(self):
        tomorrow = timezone.now() + timedelta(days=1)
        self.track = mommy.make(Track, event__due_date=tomorrow)

    def test_check_if_track_has_activities(self):
        self.assertFalse(self.track.has_activities())

        mommy.make('deck.Activity', track=self.track)

        self.assertTrue(self.track.has_activities())

    def test_refresh_track_update_tracks_proposals_and_activites(self):
        proposal = mommy.make(Proposal, is_approved=True, track=self.track, event=self.track.event)
        activity = mommy.make('deck.Activity', track=self.track, track_order=10)

        self.track.refresh_track()
        proposal.refresh_from_db()
        activity.refresh_from_db()

        self.assertFalse(proposal.is_approved)
        self.assertIsNone(activity.track)
        self.assertIsNone(activity.track_order)

    def test_add_proposal_to_slot_updates_proposal_state(self):
        proposal = mommy.make(Proposal, track=None, event=self.track.event)

        self.track.add_proposal_to_slot(proposal, 3)
        proposal.refresh_from_db()

        self.assertEqual(proposal.track, self.track)
        self.assertEqual(proposal.track_order, 3)
        self.assertTrue(proposal.is_approved)

    def test_add_general_activity_to_slot_updates_activity_state(self):
        activity = mommy.make(Activity, activity_type=Activity.COFFEEBREAK)

        self.track.add_activity_to_slot(activity, 3)
        activity.refresh_from_db()

        self.assertEqual(activity.track, self.track)
        self.assertEqual(activity.track_order, 3)

    @patch.object(Track, 'add_proposal_to_slot', Mock())
    def test_add_proposal_activity_to_slot_updates_activity_and_proposal_state(self):
        activity = mommy.make(Proposal, activity_type=Activity.PROPOSAL, event=self.track.event)

        self.track.add_activity_to_slot(activity, 3)
        activity.refresh_from_db()

        self.assertEqual(activity.track, self.track)
        self.assertEqual(activity.track_order, 3)
        self.track.add_proposal_to_slot.assert_called_once_with(activity.proposal, 3)


class GetActivitiesByParametersOrderTests(TestCase):

    def test_respect_ids_order(self):
        activities = mommy.make(Activity, _quantity=3)
        query = [
            activities[1].id,
            activities[2].id,
            activities[0].id,
        ]

        filtered_activities = get_activities_by_parameters_order(query)

        self.assertEqual(filtered_activities[0], activities[1])
        self.assertEqual(filtered_activities[1], activities[2])
        self.assertEqual(filtered_activities[2], activities[0])
