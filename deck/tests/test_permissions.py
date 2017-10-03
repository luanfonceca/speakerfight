from mock import patch, Mock
from model_mommy import mommy

from django.test import TestCase
from django.conf import settings

from deck.permissions import has_manage_schedule_permission
from deck.models import Event


class PermissionsTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make(settings.AUTH_USER_MODEL)
        self.event = mommy.make(Event)

    def test_super_user_is_always_allowed(self):
        self.user.is_superuser = True

        has_permission = has_manage_schedule_permission(self.user, self.event)

        self.assertTrue(has_permission)

    @patch.object(Event, 'user_in_jury', Mock(return_value=True))
    def test_regular_user_must_be_in_jury_to_permission(self):
        has_permission = has_manage_schedule_permission(self.user, self.event)

        self.assertTrue(has_permission)
        self.event.user_in_jury.assert_called_once_with(self.user)
