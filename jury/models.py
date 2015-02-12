from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings


class Jury(models.Model):
    # relations
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                   related_name='juries')

    class Meta:
        verbose_name = _('Jury')
        verbose_name_plural = _('Juries')
