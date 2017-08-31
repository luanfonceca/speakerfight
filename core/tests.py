# coding: utf-8

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from core.models import Profile


class AboutViewTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/about/')

    def test_get(self):
        'GET /about/ must return status code 200'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'About page must use about.html'
        self.assertTemplateUsed(self.resp, 'about.html')


class ProfileUpdateTest(TestCase):
    fixtures = ['user.json', 'event.json', 'proposal.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username='user', password='user')

        self.profile = Profile.objects.get(user__username='user')
        self.profile_data = {
            'username': self.profile.user.username,
            'name': self.profile.user.get_full_name(),
            'email': self.profile.user.email,
            'about_me': '',
            'github': '',
            'facebook': '',
            'site': '',
        }

    def test_update_profile_username(self):
        new_profile_data = self.profile_data.copy()
        new_profile_data['username'] = 'new_username'

        response = self.client.post(
            reverse('update_profile', kwargs={
                'user__username': self.profile.user.username
            }),
            new_profile_data, follow=True)

        self.assertEquals(200, response.status_code)
        new_profile = response.context['profile']
        self.assertEquals('new_username', new_profile.user.username)

    def test_update_profile_name(self):
        new_profile_data = self.profile_data.copy()
        new_profile_data['name'] = 'User Full Name'

        response = self.client.post(
            reverse('update_profile', kwargs={
                'user__username': self.profile.user.username
            }),
            new_profile_data, follow=True)

        self.assertEquals(200, response.status_code)
        new_profile = response.context['profile']
        self.assertEquals('User Full Name', new_profile.user.get_full_name())

    def test_update_profile_site(self):
        new_profile_data = self.profile_data.copy()
        new_profile_data['site'] = 'https://speakerfight.com/profile/'

        response = self.client.post(
            reverse('update_profile', kwargs={
                'user__username': self.profile.user.username
            }),
            new_profile_data, follow=True)

        self.assertEquals(200, response.status_code)
        new_profile = response.context['profile']
        self.assertEquals('https://speakerfight.com/profile/', new_profile.site)

    def test_events_on_profile(self):
        response = self.client.get(
            reverse('user_profile', kwargs={
                'user__username': self.profile.user.username
            }), follow=True)

        self.assertEquals(200, response.status_code)
        self.assertQuerysetEqual(response.context['events'],
                                 ["<Event: RuPy Natal>"])

    def test_proposals_on_profile(self):
        self.client.logout()
        self.client.login(username='admin', password='admin')

        response = self.client.get(
            reverse('user_profile', kwargs={
                'user__username': self.profile.user.username
            }), follow=True)

        self.assertEquals(200, response.status_code)
        exceped_proposals = [
            '<Proposal: Django Vanilla Views>',
            '<Proposal: Flask is Fun>',
        ]
        self.assertQuerysetEqual(response.context['proposals'],
                                 exceped_proposals)
