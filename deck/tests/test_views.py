from mock import patch, Mock
from model_mommy import mommy
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from deck.forms import ActivityForm, ActivityTimetableForm


class CreateEventScheduleViewTests(TestCase):

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
