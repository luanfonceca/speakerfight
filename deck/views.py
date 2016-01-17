# -*- encoding: utf-8 -*
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError, models
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from vanilla import CreateView, DeleteView, DetailView, ListView, UpdateView
from djqscsv import render_to_csv_response

from .models import Event, Proposal, Vote, Activity
from .forms import EventForm, ProposalForm, ActivityForm, ActivityTimetableForm
from core.mixins import LoginRequiredMixin, FormValidRedirectMixing


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


class CreateEvent(LoginRequiredMixin,
                  BaseEventView,
                  CreateView,
                  FormValidRedirectMixing):
    template_name = 'event/event_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        if settings.SEND_NOTIFICATIONS:
            self.send_event_creation_email()

        return self.success_redirect(_(u'Event created.'))

    def send_event_creation_email(self):
        event = self.object
        context = {'event_title': event.title}
        message = render_to_string('mailing/event_created.txt', context)
        subject = _(u'Your event is ready to receive proposals')
        send_mail(subject, message,
                  settings.NO_REPLY_EMAIL, [event.author.email])


class DetailEvent(BaseEventView, DetailView):
    template_name = 'event/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailEvent, self).get_context_data(**kwargs)
        context['vote_rates'] = Vote.VOTE_RATES
        event_proposals = self.object.proposals.cached_authors()
        if self.object.user_can_see_proposals(self.request.user):
            if not self.request.user.is_anonymous():
                event_proposals = event_proposals.order_by_never_voted(
                    user_id=self.request.user.id)
        elif not self.request.user.is_anonymous():
            event_proposals = event_proposals.filter(author=self.request.user)
        else:
            event_proposals = event_proposals.none()
        context.update(event_proposals=event_proposals)
        return context


class ListMyEvents(LoginRequiredMixin, BaseEventView, ListView):
    template_name = 'event/my_events.html'

    def get_queryset(self):
        return Event.objects.filter(author_id=self.request.user.id)


class UpdateEvent(BaseEventView, UpdateView, FormValidRedirectMixing):
    template_name = 'event/event_form.html'

    def form_valid(self, form):
        self.object = form.save()
        return self.success_redirect(_(u'Event updated.'))

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
            'author__username': _('Author'),
            'author__email': _('Author E-Mail'),
            'votes__rate__sum': _('Vote Rate'),
            'votes__count': _('Votes Count'),
        }
        proposals = event.get_votes_to_export()
        return render_to_csv_response(
            proposals,
            append_datestamp=True,
            filename=filename,
            field_header_map=field_header_map
        )


class CreateEventSchedule(BaseEventView, DetailView):
    template_name = 'event/event_create_schedule.html'

    def get_context_data(self, **kwargs):
        context = super(CreateEventSchedule, self).get_context_data(**kwargs)
        context.update(activity_form=ActivityForm())
        context.update(activity_timetable_form=ActivityTimetableForm())
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        in_jury = self.object.jury.users.filter(
            pk=self.request.user.pk).exists()
        if (not in_jury and not self.request.user.is_superuser):
            messages.error(
                self.request, _(u'You are not allowed to see this page.'))
            return HttpResponseRedirect(
                reverse('view_event', kwargs={'slug': self.object.slug}),
            )
        return super(CreateEventSchedule, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        track = self.object.tracks.first()

        # On the first time we generate a schedule based on the Slots.
        if not track.activities.exists():
            top_not_approved_ones = self.object.get_not_approved_schedule()
            order = 0
            for proposal in top_not_approved_ones[:self.object.slots]:
                proposal.track = track
                proposal.is_approved = True
                proposal.track_order = order
                proposal.save()
                order += 1
        return super(CreateEventSchedule, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        approved_activities_pks = self.request.POST.getlist(
            'approved_activities')

        track = self.object.tracks.first()
        track.proposals.update(is_approved=False)
        track.activities.update(track=None, track_order=None)

        if not approved_activities_pks:
            return HttpResponseRedirect(
                reverse('create_event_schedule',
                        kwargs={'slug': self.object.slug}),
            )

        order = 0
        for activity_pk in approved_activities_pks:
            activity = Activity.objects.get(pk=activity_pk)
            activity.track = track
            activity.track_order = order
            activity.save()
            if activity.activity_type == Activity.PROPOSAL:
                activity.proposal.is_approved = True
                activity.proposal.save()
            order += 1

        return HttpResponseRedirect(
            reverse('create_event_schedule',
                    kwargs={'slug': self.object.slug}),
        )


class DetailEventSchedule(BaseEventView, DetailView):
    template_name = 'event/event_detail_schedule.html'


class BaseProposalView(object):
    model = Proposal
    form_class = ProposalForm
    lookup_field = 'slug'


class CreateProposal(LoginRequiredMixin,
                     BaseProposalView,
                     CreateView,
                     FormValidRedirectMixing):
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
                _(u"This Event doesn't accept Proposals anymore."))
            return HttpResponseRedirect(
                reverse('view_event', kwargs={'slug': event.slug}),
            )
        return super(CreateProposal, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.event = Event.objects.get(slug=self.kwargs['slug'])
        self.object.save()
        for coauthor in form.data.get("coauthors", []):
            self.object.coauthors.add(coauthor)
        if settings.SEND_NOTIFICATIONS:
            self.send_new_proposal_to_jury_email()
            self.send_proposal_creation_email()
        return self.success_redirect(_(u'Proposal created.'))

    def send_new_proposal_to_jury_email(self):
        proposal = self.object
        context = {
            'event_title': proposal.event.title,
            'proposal_title': proposal.title
        }
        message = render_to_string('mailing/jury_new_proposal.txt', context)
        subject = _(u'Your event has new proposals')
        recipients = proposal.event.jury.users.values_list('email', flat=True)
        send_mail(subject, message, settings.NO_REPLY_EMAIL, recipients)

    def send_proposal_creation_email(self):
        proposal = self.object
        context = {
            'event_title': proposal.event.title,
            'proposal_title': proposal.title
        }
        message = render_to_string(
            'mailing/author_proposal_created.txt', context)
        subject = _(u'Your proposal was submitted')
        recipients = proposal.get_authors_email()
        send_mail(subject, message, settings.NO_REPLY_EMAIL, recipients)


class ListMyProposals(LoginRequiredMixin, BaseProposalView, ListView):
    template_name = 'proposal/my_proposals.html'

    def get_queryset(self):
        return Proposal.objects.filter(author_id=self.request.user.id)


class UpdateProposal(LoginRequiredMixin,
                     BaseProposalView,
                     UpdateView,
                     FormValidRedirectMixing):
    template_name = 'proposal/proposal_form.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateProposal, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug=self.kwargs['event_slug'])
        return context

    def form_valid(self, form):
        self.object = form.save()
        return self.success_redirect(_(u'Proposal updated.'))


class DeleteProposal(BaseProposalView, DeleteView):
    template_name = 'proposal/proposal_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        proposal = self.get_object()
        proposal.delete()
        messages.success(self.request, _(u'Proposal deleted.'))
        return HttpResponseRedirect(proposal.event.get_absolute_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        proposal = self.get_object()
        if (proposal.author != self.request.user and
           not self.request.user.is_superuser):
            messages.error(
                self.request, _(u'You are not allowed to see this page.'))
            return HttpResponseRedirect(proposal.event.get_absolute_url())
        return super(DeleteProposal, self).dispatch(*args, **kwargs)


class RateProposal(BaseProposalView, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        rate = kwargs.get('rate')
        response_content = {}
        response_status = 200

        try:
            self.object.rate(self.request.user, rate)
        except IndexError:
            response_content['message'] = _(u'Rate Index not found.')
            response_status = 400
        except (IntegrityError, ValidationError), e:
            response_content['message'] = e.message
            response_status = 400
        else:
            response_content['message'] = _(u'Proposal rated.')
        return HttpResponse(
            json.dumps(response_content),
            status=response_status,
            content_type='application/json')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        rate = kwargs.get('rate')

        try:
            self.object.rate(self.request.user, rate)
        except IndexError:
            messages.error(self.request, _(u'Rate Index not found.'))
        except (IntegrityError, ValidationError), e:
            messages.error(self.request, e.message)
        else:
            messages.success(self.request, _(u'Proposal rated.'))
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, *args, **kwargs):
        proposal = self.get_object()
        view_event_url = reverse(
            'view_event', kwargs={'slug': proposal.event.slug})

        if not self.request.user.is_authenticated():
            message = _(u'You need to be logged in to '
                        u'continue to the next step.')
            if self.request.method == 'GET':
                messages.error(self.request, message)
                return HttpResponseRedirect(view_event_url)
            response = {}
            response['message'] = message
            response['redirectUrl'] = u'{}?{}={}'.format(
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
                self.request.META.get('PATH_INFO')
            )
            return HttpResponse(
                json.dumps(response),
                status=401,
                content_type='application/json')
        elif not proposal.user_can_vote(self.request.user):
            message = _(u'You are not allowed to see this page.')
            if self.request.method == 'GET':
                messages.error(self.request, message)
                return HttpResponseRedirect(view_event_url)
            response = {}
            response['message'] = message
            response['redirectUrl'] = ''
            return HttpResponse(
                json.dumps(response),
                status=401,
                content_type='application/json'
            )
        return super(RateProposal, self).dispatch(*args, **kwargs)


class ApproveProposal(BaseProposalView, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response_content = {}
        response_status = 200

        try:
            self.object.approve()
        except (IntegrityError, ValidationError), e:
            response_content['message'] = e.message
            response_status = 400
        else:
            response_content['message'] = _(u'Proposal approved.')
        return HttpResponse(
            json.dumps(response_content),
            status=response_status,
            content_type='application/json')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.approve()
        except (IntegrityError, ValidationError), e:
            messages.error(self.request, e.message)
        else:
            messages.success(self.request, _(u'Proposal approved.'))
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, *args, **kwargs):
        proposal = self.get_object()
        view_event_url = reverse(
            'view_event', kwargs={'slug': proposal.event.slug})

        if not self.request.user.is_authenticated():
            message = _(u'You need to be logged in to '
                        u'continue to the next step.')
            if self.request.method == 'GET':
                messages.error(self.request, message)
                return HttpResponseRedirect(view_event_url)
            response = {}
            response['message'] = message
            response['redirectUrl'] = u'{}?{}={}'.format(
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
                self.request.META.get('PATH_INFO')
            )
            return HttpResponse(
                json.dumps(response),
                status=401,
                content_type='application/json')
        elif not proposal.user_can_approve(self.request.user):
            message = _(u'You are not allowed to see this page.')
            if self.request.method == 'GET':
                messages.error(self.request, message)
                return HttpResponseRedirect(view_event_url)
            response = {}
            response['message'] = message
            response['redirectUrl'] = ''
            return HttpResponse(
                json.dumps(response),
                status=401,
                content_type='application/json'
            )
        return super(ApproveProposal, self).dispatch(*args, **kwargs)


class DisapproveProposal(BaseProposalView, UpdateView):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response_content = {}
        response_status = 200

        try:
            self.object.disapprove()
        except (IntegrityError, ValidationError), e:
            response_content['message'] = e.message
            response_status = 400
        else:
            response_content['message'] = _(u'Proposal disapproved.')
        return HttpResponse(
            json.dumps(response_content),
            status=response_status,
            content_type='application/json')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.disapprove()
        except (IntegrityError, ValidationError), e:
            messages.error(self.request, e.message)
        else:
            messages.success(self.request, _(u'Proposal disapproved.'))
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, *args, **kwargs):
        proposal = self.get_object()
        view_event_url = reverse(
            'view_event', kwargs={'slug': proposal.event.slug})

        if not self.request.user.is_authenticated():
            message = _(u'You need to be logged in to '
                        u'continue to the next step.')
            if self.request.method == 'GET':
                messages.error(self.request, message)
                return HttpResponseRedirect(view_event_url)
            response = {}
            response['message'] = message
            response['redirectUrl'] = u'{}?{}={}'.format(
                settings.LOGIN_URL,
                REDIRECT_FIELD_NAME,
                self.request.META.get('PATH_INFO')
            )
            return HttpResponse(
                json.dumps(response),
                status=401,
                content_type='application/json')
        elif not proposal.user_can_approve(self.request.user):
            message = _(u'You are not allowed to see this page.')
            if self.request.method == 'GET':
                messages.error(self.request, message)
                return HttpResponseRedirect(view_event_url)
            response = {}
            response['message'] = message
            response['redirectUrl'] = ''
            return HttpResponse(
                json.dumps(response),
                status=401,
                content_type='application/json'
            )
        return super(DisapproveProposal, self).dispatch(*args, **kwargs)
