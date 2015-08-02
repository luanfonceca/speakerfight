from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


from deck.forms import InviteForm
from deck.models import Event


class InviteFormTestCase(TestCase):
    fixtures = ['user.json', 'event.json']

    def setUp(self):
        self.author = User.objects.get(username='user')
        self.event = Event.objects.first()

    def test_user_should_be_added_as_jury_to_event(self):
        self.assertEqual(self.event.jury.users.count(), 1)
        form = InviteForm(instance=self.event,
                          data={'email': 'another@speakerfight.com'})
        form.is_valid()
        form.add_to_jury()

        self.assertEqual(self.event.jury.users.count(), 2)

    def test_inexistent_user_should_raise_exception(self):
        form = InviteForm(instance=self.event,
                          data={'email': 'usernotfound@speakerfight.com'})
        form.is_valid()
        with self.assertRaises(ValidationError):
            form.add_to_jury()

    def test_user_already_a_jury_should_not_be_added_as_jury_to_event(self):
        form = InviteForm(instance=self.event,
                          data={'email': 'user@speakerfight.com'})
        form.is_valid()
        with self.assertRaises(ValidationError):
            form.add_to_jury()
