from mock import patch
from model_mommy import mommy
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from django.utils import timezone


class CreateEventScheduleViewTests(TestCase):

    def setUp(self):
        tomorrow = timezone.now() + timedelta(days=1)
        self.event = mommy.make('deck.Event', due_date=tomorrow)
        self.url = reverse('create_event_schedule', args=[self.event.slug])


    @patch('deck.views.has_manage_schedule_permission')
    def test_redirect_to_view_event_if_user_does_not_have_permission_to_manage_schedule(self, mocked_permission):
        mocked_permission.return_value = False
        # Request Setup
        user = mommy.make(settings.AUTH_USER_MODEL)
        self.client.force_login(user)

        # HTTP Request
        response = self.client.get(self.url)
        redirect_url = reverse('view_event', args=[self.event.slug])

        self.assertRedirects(response, redirect_url)
        mocked_permission.assert_called_once_with(user, self.event)
