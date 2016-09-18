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
    fixtures = ['user.json']

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
        new_profile_data['site'] = 'http://speakerfight.com/profile/'

        response = self.client.post(
            reverse('update_profile', kwargs={
                'user__username': self.profile.user.username
            }),
            new_profile_data, follow=True)

        self.assertEquals(200, response.status_code)
        new_profile = response.context['profile']
        self.assertEquals('http://speakerfight.com/profile/', new_profile.site)
