from django.test import TestCase, Client
from django.core.urlresolvers import reverse
# from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from deck.tests.test_unit import EVENT_DATA
from deck.models import Event


class JuryTest(TestCase):
    fixtures = ['user.json', 'socialapp.json']

    def setUp(self):
        self.client = Client()
        self.event_data = EVENT_DATA.copy()
        self.client.login(username='admin', password='admin')

    def test_event_invite_to_jury(self):
        event = Event.objects.create(**self.event_data)
        user = User.objects.get(username='user')
        invite_url = reverse('event_invite_to_jury',
                             kwargs={'slug': event.slug})
        response = self.client.post(invite_url,
                                    {'email': user.email},
                                    follow=True)

        message = _(u'The "@%s" are successfully joined to the Jury.') % user
        self.assertIn(message, response.content)
        self.assertEquals(2, event.jury.users.count())
        self.assertQuerysetEqual(event.jury.users.all(),
                                 ['<User: admin>', '<User: user>'],
                                 ordered=False)

    def test_event_invite_to_jury_an_already_joined_user(self):
        event = Event.objects.create(**self.event_data)
        email = {'email': 'admin@speakerfight.com'}
        invite_url = reverse('event_invite_to_jury',
                             kwargs={'slug': event.slug})
        response = self.client.post(invite_url, email, follow=True)

        message = _(u'The "@admin" already is being part of this jury.')
        self.assertIn(message, response.content)
        self.assertEquals(1, event.jury.users.count())
        self.assertQuerysetEqual(event.jury.users.all(),
                                 ['<User: admin>'],
                                 ordered=False)

    def test_event_invite_to_jury_a_not_speakerfight_user(self):
        event = Event.objects.create(**self.event_data)
        email = {'email': 'new_user@speakerfight.com'}
        invite_url = reverse('event_invite_to_jury',
                             kwargs={'slug': event.slug})
        response = self.client.post(invite_url, email, follow=True)

        message = _(u'The "new_user@speakerfight.com" are not a Speakerfight '
                    u'user. For now, we just allow already joined users.')
        self.assertIn(message, response.content)
        self.assertEquals(1, event.jury.users.count())
        self.assertQuerysetEqual(event.jury.users.all(),
                                 ['<User: admin>'],
                                 ordered=False)

    def test_event_remove_from_jury(self):
        event = Event.objects.create(**self.event_data)
        user = User.objects.get(username='user')
        event.jury.users.add(user)

        remove_from_jury = reverse('event_remove_from_jury',
                                   kwargs={'slug': event.slug,
                                           'user_pk': user.pk})
        response = self.client.post(remove_from_jury,
                                    {'email': user.email},
                                    follow=True)
        message = _(u'The "@user" was successfully removed from the Jury.')
        self.assertIn(message, response.content)
        self.assertEquals(1, event.jury.users.count())
        self.assertQuerysetEqual(event.jury.users.all(),
                                 ['<User: admin>'],
                                 ordered=False)
