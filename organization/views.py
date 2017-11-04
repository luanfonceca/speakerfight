# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . models import Organization
from core.mixins import LoginRequiredMixin, FormValidRedirectMixing


class OwnerRequiredMixin(object):

    def dispatch(self, *args, **kwargs):
        """Only owners can manage organizations."""
        organization = self.get_object()
        if self.request.user != organization.created_by \
                and not self.request.user.is_superuser:
            raise Http404
        return super(OwnerRequiredMixin, self).dispatch(*args, **kwargs)


class BaseOrganizationView(LoginRequiredMixin, FormValidRedirectMixing):
    model = Organization
    fields = ['name', 'about']
    template_Name = 'organization/organization_form.html'

    def get_success_url(self):
        return reverse('update_organization', kwargs={'slug': self.object.slug})


class CreateOrganization(BaseOrganizationView, CreateView):
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return self.success_redirect(_(u'Organization created.'))


class UpdateOrganization(OwnerRequiredMixin, BaseOrganizationView, UpdateView):

    def form_valid(self, form):
        self.object = form.save()
        return self.success_redirect(_(u'Organization updated.'))


class DeleteOrganization(OwnerRequiredMixin, BaseOrganizationView, DeleteView):
    template_Name = 'organization/organization_confirm_delete.html'

    def form_valid(self, form):
        return self.success_redirect(_(u'Organization deleted.'))

    def get_success_url(self):
        # TODO: Redirect to the organization list route when it gets done
        return reverse('list_events')
