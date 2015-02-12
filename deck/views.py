from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models, transaction
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from vanilla import CreateView, ListView, UpdateView, DetailView

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
        if (self.request.user.is_superuser or self.object.author == self.request.user): 
            # Admin users and event authors can see all proposals.
            pass
        elif (not self.object.allow_public_voting and
              self.request.user.is_authenticated()):
            event_proposals = event_proposals.filter(author=self.request.user)
        elif (self.object.allow_public_voting and
              self.request.user.is_authenticated()):
            event_proposals = event_proposals.filter(
                models.Q(is_published=True) |
                models.Q(author=self.request.user))
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
        if event.author != self.request.user:
            messages.error(
                self.request, _(u'You are not allowed to see this page.'))
            return HttpResponseRedirect(
                reverse('view_event', kwargs={'slug': event.slug}),
            )
        return super(UpdateEvent, self).dispatch(*args, **kwargs)


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

        try:
            rate_int = [r[0] for r in Vote.VOTE_RATES if rate in r][0]
            with transaction.atomic():
                self.object.votes.create(user=request.user, rate=rate_int)
        except IndexError:
            messages.error(self.request, _(u'Rate Index not found.'))
        except (IntegrityError, ValidationError), e:
            messages.error(self.request, e.message)
        else:
            messages.success(self.request, _(u'Proposal rated.'))
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RateProposal, self).dispatch(*args, **kwargs)
