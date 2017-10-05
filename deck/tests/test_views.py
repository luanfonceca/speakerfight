from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from mock import patch, Mock
from model_mommy import mommy
from datetime import timedelta

from deck.exceptions import EmptyActivitiesArrangementException
from deck.forms import ActivityForm, ActivityTimetableForm
from deck.models import Activity, Vote


class CreateEventScheduleViewTests(TestCase):

    def assertSingleMessage(self, response, msg, level):
        self.assertEqual(1, len(response.context['messages']))
        for message in response.context['messages']:
            self.assertEqual(msg, message.message)
            self.assertEqual(level, message.level)

    def setUp(self):
        tomorrow = timezone.now() + timedelta(days=1)
        # DB Setup
        self.event = mommy.make('deck.Event', due_date=tomorrow)
        self.url = reverse('create_event_schedule', args=[self.event.slug])
        # Request Setup
        self.user = mommy.make(settings.AUTH_USER_MODEL)
        self.client.force_login(self.user)

    @patch('deck.views.has_manage_schedule_permission')
    def test_redirect_to_view_event_if_user_does_not_have_permission_to_manage_schedule(self, mocked_permission):
        mocked_permission.return_value = False

        # HTTP Request
        response = self.client.get(self.url)
        redirect_url = reverse('view_event', args=[self.event.slug])

        self.assertRedirects(response, redirect_url)
        mocked_permission.assert_called_once_with(self.user, self.event)

    @patch('deck.views.has_manage_schedule_permission', Mock(return_value=True))
    @patch('deck.views.initialize_event_schedule')
    def test_initialize_event_schedule_for_allowed_user(self, mocked_use_case):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_create_schedule.html')
        mocked_use_case.assert_called_once_with(self.event)

    @patch('deck.views.has_manage_schedule_permission', Mock(return_value=True))
    @patch('deck.views.initialize_event_schedule', Mock())
    def test_returns_correct_context_to_html(self):
        response = self.client.get(self.url)

        self.assertEqual(self.event, response.context['event'])
        self.assertIsInstance(response.context['activity_form'], ActivityForm)
        self.assertIsInstance(response.context['activity_timetable_form'], ActivityTimetableForm)

    def test_login_required(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(settings.LOGIN_URL, response['Location'])

    def test_404_if_event_does_not_exist(self):
        self.event.delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    @patch('deck.views.has_manage_schedule_permission', Mock(return_value=True))
    @patch('deck.views.get_activities_by_parameters_order')
    @patch('deck.views.rearrange_event_schedule')
    def test_rearrange_event_with_post_order(self, mocked_use_case, mocked_query_method):
        activities = mommy.make(Activity, _quantity=3)
        mocked_query_method.return_value = activities
        post_data = {'approved_activities': [1, 2, 3]}

        response = self.client.post(self.url, post_data)

        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        mocked_query_method.assert_called_once_with(['1', '2', '3'])
        mocked_use_case.assert_called_once_with(self.event, activities)

    @patch('deck.views.has_manage_schedule_permission', Mock(return_value=True))
    @patch('deck.views.get_activities_by_parameters_order', Mock(return_value=[]))
    @patch('deck.views.rearrange_event_schedule', Mock(side_effect=EmptyActivitiesArrangementException))
    @patch('deck.views.initialize_event_schedule', Mock())
    def test_redirect_back_to_create_event_on_exception(self):
        post_data = {'approved_activities': []}

        response = self.client.post(self.url, post_data, follow=True)

        error_msg = u'You must pass at least one activity.'
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        self.assertSingleMessage(response, error_msg, messages.ERROR)

    def test_full_integration_test(self):
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
