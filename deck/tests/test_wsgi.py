from django.test import TestCase
from django.core.handlers.wsgi import WSGIHandler

from os import environ

from speakerfight.wsgi import application


class WSGITest(TestCase):
    def test_assert_django_settings_module(self):
        self.assertEquals('speakerfight.settings',
                          environ.get('DJANGO_SETTINGS_MODULE'))

    def test_assert_application(self):
        self.assertIsInstance(application, WSGIHandler)
