# -*- encoding: utf-8 -*
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models, transaction
from django.db.models.aggregates import Sum
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from vanilla import CreateView, ListView, UpdateView, DetailView
from djqscsv import render_to_csv_response

from .models import Event, Proposal, Vote
from .forms import (EventForm, ProposalForm)


class BaseEventView(object):
    model = Event
    form_class = EventForm
    lookup_field = 'slug'


class ListEvents(BaseEventView, ListView):
    template_name = 'event/event_list.html'
    queryset = Event.objects.published_ones()

    def get_context_data(self, **kwargs):
        context = super(ListEvents, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            event_list = Event.objects.filter(
                models.Q(is_published=True) |
                models.Q(author=self.request.user))
            context.update(event_list=event_list)
        return context


class CreateEvent(BaseEventView, CreateView):
    template_name = 'event/event_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, _(u'Event created.'))
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateEvent, self).dispatch(*args, **kwargs)


class DetailEvent(BaseEventView, DetailView):
    template_name = 'event/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailEvent, self).get_context_data(**kwargs)
        context['vote_rates'] = Vote.VOTE_RATES
        event_proposals = self.object.proposals.cached_authors()
        if self.object.user_can_see_proposals(self.request.user):
            pass
        elif not self.request.user.is_anonymous():
            event_proposals = event_proposals.filter(author=self.request.user)
        else:
            event_proposals = event_proposals.none()
        context.update(event_proposals=event_proposals)
        return context


class UpdateEvent(BaseEventView, UpdateView):
    template_name = 'event/event_form.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _(u'Event updated.'))
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        event = self.get_object()
        if (event.author != self.request.user and
           not self.request.user.is_superuser):
            messages.error(
                self.request, _(u'You are not allowed to see this page.'))
            return HttpResponseRedirect(
                reverse('view_event', kwargs={'slug': event.slug}),
            )
        return super(UpdateEvent, self).dispatch(*args, **kwargs)


class ExportEvent(BaseEventView, DetailView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        event = self.get_object()
        if (event.author != self.request.user and
           not self.request.user.is_superuser):
            messages.error(
                self.request, _(u'You are not allowed to see this page.'))
            return HttpResponseRedirect(reverse('list_events'))
        return super(ExportEvent, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        event = self.get_object()
        filename = "event_%s_export" % event.slug.replace('-', '_')
        field_header_map = {
            'author__username': 'Author',
            'votes__rate__sum': 'Votes'
        }
        proposals = event.proposals.values(
            'id', 'title', 'author__username').annotate(Sum('votes__rate'))
        return render_to_csv_response(
            proposals,
            append_datestamp=True,
            filename=filename,
            field_header_map=field_header_map
        )


class BaseProposalView(object):
    model = Proposal
    form_class = ProposalForm
    lookup_field = 'slug'


class CreateProposal(BaseProposalView, CreateView):
    template_name = 'proposal/proposal_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProposal, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug=self.kwargs['slug'])
        return context

    def get(self, request, *args, **kwargs):
        data = self.get_context_data()
        event = data.get('event')
        if event.due_date_is_passed:
            messages.error(
                self.request,
                _("This Event doesn't accept Proposals anymore."))
            return HttpResponseRedirect(
                reverse('view_event', kwargs={'slug': event.slug}),
            )
        return super(CreateProposal, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.event = Event.objects.get(slug=self.kwargs['slug'])
        self.object.save()
        messages.success(self.request, _(u'Proposal created.'))
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateProposal, self).dispatch(*args, **kwargs)


class UpdateProposal(BaseProposalView, UpdateView):
    template_name = 'proposal/proposal_form.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateProposal, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug=self.kwargs['event_slug'])
        return context

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, _(u'Proposal updated.'))
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateProposal, self).dispatch(*args, **kwargs)


class RateProposal(BaseProposalView, UpdateView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        rate = kwargs.get('rate')
        response_content = {}
        response_status = 200

        try:
            rate_int = [r[0] for r in Vote.VOTE_RATES if rate in r][0]
            with transaction.atomic():
                self.object.votes.create(user=request.user, rate=rate_int)
        except IndexError:
            response_content['errorMessage'] = _(u'Rate Index not found.')
            response_status = 400
        except (IntegrityError, ValidationError), e:
            response_content['errorMessage'] = e.message
            response_status = 400
        else:
            response_content['message'] = _(u'Proposal rated.')
        return HttpResponse(
            json.dumps(response_content),
            status=response_status,
            content_type='application/json')

    def dispatch(self, *args, **kwargs):
        proposal = self.get_object()

        if not self.request.user.is_authenticated():
            response = {}
            response['errorMessage'] = _(u' You need to be logged in to continue to the next step.')
            response['redirectUrl'] = u'{}?{}={}'.format(
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
                reverse('view_event', kwargs={'slug': proposal.event.slug})
            )
            return HttpResponse(json.dumps(response), status=401, content_type='application/json')

        if not proposal.user_can_vote(self.request.user):
            response = {}
            response['errorMessage'] = _(u'You are not allowed to see this page.')
            response['redirectUrl'] = ''
            return HttpResponse(json.dumps(response), status=401, content_type='application/json')
        return super(RateProposal, self).dispatch(*args, **kwargs)
