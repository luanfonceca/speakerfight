# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.conf import settings

from django_extensions.db.fields import AutoSlugField


@python_2_unicode_compatible
class Organization(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = AutoSlugField(populate_from='name', overwrite=True,
                         max_length=200, unique=True, db_index=True)
    about = models.TextField(
        _('About'), max_length=10000, blank=True)

    # relations
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='organizations'
    )

    def __str__(self):
        return six.text_type(self.name)
