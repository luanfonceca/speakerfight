from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core import mail
from django.conf import settings

from vanilla import TemplateView, DetailView, UpdateView, FormView

from deck.models import Event, Proposal
from core.models import Profile
from core.forms import ProfileForm, FeedbackForm
from core.mixins import LoginRequiredMixin, FormValidRedirectMixing


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            events=Event.objects.count(),
            proposals=Proposal.objects.count(),
            users=User.objects.count()
        )
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ProfileView(DetailView):
    template_name = 'account/profile.html'
    model = Profile
    lookup_field = 'user__username'

    def get_object(self, **kwargs):
        queryset = self.get_queryset()
        username = self.kwargs.get('user__username')

        if not username and self.request.user.is_authenticated():
            return self.request.user.profile
        else:
            return get_object_or_404(queryset, user__username=username)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update(profile_form=ProfileForm(instance=self.get_object()))
        return context


class ProfileUpdateView(LoginRequiredMixin,
                        FormValidRedirectMixing,
                        UpdateView):
    template_name = 'account/profile.html'
    model = Profile
    form_class = ProfileForm
    lookup_field = 'user__username'

    def get_object(self, **kwargs):
        queryset = self.get_queryset()
        username = self.kwargs.get('user__username')

        if not username and self.request.user.is_authenticated():
            return self.request.user.profile
        elif (username == self.request.user.username or
              self.request.user.is_superuser):
            return get_object_or_404(queryset, user__username=username)
        else:
            raise Http404

    def form_valid(self, form):
        self.object = form.save()
        return self.success_redirect(_(u'Profile updated.'))

    def get(self, *args, **kwargs):
        self.object = self.get_object()

        return HttpResponseRedirect(
            self.object.get_absolute_url()
        )

    def form_invalid(self, form):
        for error in form.errors.itervalues():
            messages.error(self.request, error.as_data()[0].message)

        return self.get()


class FeedbackView(LoginRequiredMixin, FormView):
    template_name = 'feedback.html'
    form_class = FeedbackForm

    def form_valid(self, form):
        message = mail.EmailMessage(form.cleaned_data['subject'],
                                    form.cleaned_data['message'],
                                    settings.NO_REPLY_EMAIL,
                                    [settings.FEEDBACK_EMAIL],
                                    headers={'Reply-To': self.request.user.email})
        message.send()
        messages.success(self.request, _('Thank you for your feedback! We\'ll get in touch as soon as possible.'))
        return HttpResponseRedirect('/events/')
