from django.test import TestCase
from django.core.urlresolvers import reverse


class EventUrlTest(TestCase):
    def setUp(self):
        self.url_kwargs = {
            'slug': 'rupy'
        }

    def test_assert_event_should_have_an_absolute_url(self):
        self.assertEquals(
            '/events/rupy/',
            reverse('view_event', kwargs=self.url_kwargs)
        )

    def test_assert_event_should_have_an_update_url(self):
        self.assertEquals(
            '/events/rupy/update/',
            reverse('update_event', kwargs=self.url_kwargs)
        )

    def test_assert_event_should_have_an_create_event_proposal_url(self):
        self.assertEquals(
            '/events/rupy/proposals/create/',
            reverse('create_event_proposal', kwargs=self.url_kwargs)
        )


class ProposalUrlTest(TestCase):
    def setUp(self):
        self.url_kwargs = {
            'slug': 'python-for-zombies',
            'event_slug': 'rupy'
        }

    def test_assert_proposal_should_have_an_rate_url(self):
        kwargs = self.url_kwargs.copy()
        kwargs.update(rate=1)
        self.assertEquals(
            '/events/rupy/proposals/python-for-zombies/rate/1',
            reverse('rate_proposal', kwargs=kwargs)
        )
