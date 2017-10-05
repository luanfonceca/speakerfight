from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from organization.models import Organization


class OrganizationTest(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.get(username='user')
        self.client = Client()
        self.client.login(username='user', password='user')

    def test_create_event(self):
        url = reverse('create_organization')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'name': 'Speakerfight Corp', 'about': 'Cool company'}
        url = reverse('create_organization')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('update_organization', kwargs={'slug': 'speakerfight-corp'})
        )
        self.assertEqual(Organization.objects.count(), 1)
        organization = Organization.objects.get(slug='speakerfight-corp')
        self.assertEqual(organization.name, 'Speakerfight Corp')
        self.assertEqual(organization.about, 'Cool company')
        self.assertEqual(organization.created_by, self.user)

    def test_update_event(self):
        organization = Organization.objects.create(
            name='Speakerfight Corp',
            about='Cool company',
            created_by=self.user,
        )
        url = reverse('update_organization', kwargs={'slug': 'speakerfight-corp'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'name': 'Speakerfight School', 'about': 'Cool school'}
        url = reverse('update_organization', kwargs={'slug': 'speakerfight-corp'})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse('update_organization', kwargs={'slug': 'speakerfight-school'})
        )
        organization = Organization.objects.get(slug='speakerfight-school')
        self.assertEqual(organization.name, 'Speakerfight School')
        self.assertEqual(organization.about, 'Cool school')
