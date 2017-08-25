from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from vanilla import UpdateView

from deck.views import BaseEventView
from deck.models import Event
from .forms import InviteForm
from .models import Jury


class JuryView(UpdateView):
    template_name = 'jury/jury_detail.html'
    lookup_field = 'slug'
    model = Jury
    fields = ['users']

    def get_object(self):
        return Jury.objects.get(event__slug=self.kwargs.get('slug'))


class InviteEvent(BaseEventView, UpdateView):
    template_name = 'event/jury_invite.html'
    form_class = InviteForm

    def form_valid(self, form):
        try:
            form.add_to_jury()
        except ValidationError, e:
            messages.warning(self.request, e.message)
        else:
            user = User.objects.get(email=form.cleaned_data.get('email'))
            messages.success(
                self.request,
                _(u'The "@%s" are successfully joined to the Jury.') % user)
        return HttpResponseRedirect(
            reverse('jury_event', kwargs={'slug': self.get_object().slug}),
        )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InviteEvent, self).dispatch(*args, **kwargs)


def remove_user_from_event_jury(request, slug, user_pk):
    event = Event.objects.get(slug=slug)
    user = User.objects.get(pk=user_pk)

    event.jury.users.remove(user)

    messages.success(
        request,
        _(u'The "@%s" was successfully removed from the Jury.') % user)
    return HttpResponseRedirect(
        reverse('jury_event', kwargs={'slug': event.slug}),
    )
