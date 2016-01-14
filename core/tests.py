# coding: utf-8
from django.test import TestCase


class AboutpageTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/about/')

    def test_get(self):
        'GET / must return status code 200'
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        'About page must use about.html'
        self.assertTemplateUsed(self.resp, 'about.html')
