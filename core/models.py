from django.core.exceptions import AppRegistryNotReady
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


@python_2_unicode_compatible
class Profile(models.Model):
    about_me = models.TextField(
        _('About me'), max_length=500, null=True, blank=True)
    github = models.CharField(
        _('Github username'), max_length=50, null=True, blank=True)
    facebook = models.CharField(
        _('Facebook username'), max_length=50, null=True, blank=True)
    site = models.URLField(
        _('Site url'), max_length=200, null=True, blank=True)

    # relations
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = _('Profile')

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse_lazy(
            'user_profile', kwargs={'user__username': self.user.username})

    def get_github_url(self):
        if self.github:
            return 'http://github.com/{}'.format(self.github)

    def get_facebook_url(self):
        if self.facebook:
            return 'http://facebook.com/{}'.format(self.facebook)

    def get_site_url(self):
        return self.site


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except AppRegistryNotReady:
    from django.contrib.auth.models import User

post_save.connect(create_user_profile, sender=User)
