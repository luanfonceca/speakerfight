
from django.core.exceptions import AppRegistryNotReady
from django.urls import reverse_lazy
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from deck.models import Proposal


@python_2_unicode_compatible
class Profile(models.Model):
    language = models.CharField(
        _('Language'), choices=settings.LANGUAGES,
        max_length=50, null=True, blank=False)
    about_me = models.TextField(
        _('About me'), max_length=500, null=True, blank=True)
    github = models.CharField(
        _('Github username'), max_length=50, null=True, blank=True)
    facebook = models.CharField(
        _('Facebook username'), max_length=50, null=True, blank=True)
    twitter = models.CharField(
        _('Twitter username'), max_length=50, null=True, blank=True)
    site = models.URLField(
        _('Site url'), max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # relations
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Profile')

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse_lazy(
            'user_profile', kwargs={'user__username': self.user.username})

    def get_github_url(self):
        if self.github:
            return 'https://github.com/{}'.format(self.github)

    def get_facebook_url(self):
        if self.facebook:
            return 'https://facebook.com/{}'.format(self.facebook)

    def get_twitter_url(self):
        if self.twitter:
            return 'https://twitter.com/{}'.format(self.twitter)

    def get_site_url(self):
        return self.site

    def get_profile_events(self):
        return self.user.events.filter(is_published=True)

    def get_profile_proposals(self):
        return Proposal.objects.filter(
            author=self.user,
            event__is_published=True,
            event__anonymous_voting=False,
            is_published=True,
        )


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def slugify_user_username(sender, instance, **kwargs):
    instance.username = instance.username.replace(' ', '_')


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except AppRegistryNotReady:
    from django.contrib.auth.models import User

post_save.connect(create_user_profile, sender=User)
pre_save.connect(slugify_user_username, sender=User)
