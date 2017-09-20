
from os import environ

from django.test import TestCase

from speakerfight.wsgi import application

from whitenoise.django import DjangoWhiteNoise


class WSGITest(TestCase):
    def test_assert_django_settings_module(self):
        self.assertEquals('speakerfight.settings',
                          environ.get('DJANGO_SETTINGS_MODULE'))

    def test_assert_application(self):
        self.assertIsInstance(application, DjangoWhiteNoise)
