# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, UpdateView

from . models import Organization
from core.mixins import LoginRequiredMixin, FormValidRedirectMixing


class CreateOrganization(LoginRequiredMixin,
                         CreateView,
                         FormValidRedirectMixing):
    model = Organization
    fields = ['name', 'about']
    template_Name = 'organization/organization_form.html'

    def form_valid(self, form):
        self.object = form.save()
        return self.success_redirect(_(u'Organization created.'))

    def get_success_url(self):
        return reverse('update_organization', kwargs={'slug': self.object.slug})


class UpdateOrganization(LoginRequiredMixin,
                         UpdateView,
                         FormValidRedirectMixing):
    model = Organization
    fields = ['name', 'about']
    template_Name = 'organization/organization_form.html'

    def form_valid(self, form):
        self.object = form.save()
        return self.success_redirect(_(u'Organization updated.'))

    def get_success_url(self):
        return reverse('update_organization', kwargs={'slug': self.object.slug})
