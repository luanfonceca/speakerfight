from django.test import TestCase
from django.db.models import (ManyToManyField)
from django.contrib.auth.models import User

from jury.models import Jury
from test_utils import get_all_field_names


class JuryModelIntegrityTest(TestCase):
    def setUp(self):
        self.fields = {
            'users': Jury.users.field
        }

    def test_assert_jury_should_have_users(self):
        self.assertIn('users', get_all_field_names(Jury))

    def test_assert_jury_users_should_be_a_user(self):
        self.assertEquals(User, self.fields['users'].remote_field.model)

    def test_assert_jury_users_should_be_a_manytomanyfield(self):
        self.assertIsInstance(self.fields['users'], ManyToManyField)

    def test_assert_jury_users_should_be_required(self):
        self.assertEquals(False, self.fields['users'].null)
        self.assertEquals(False, self.fields['users'].blank)

    def test_assert_jury_event_should_have_a_related_name(self):
        self.assertEquals('juries', self.fields['users'].remote_field.get_accessor_name())
