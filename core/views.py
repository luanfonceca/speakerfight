from django.contrib.auth.models import User

from vanilla import TemplateView

from deck.models import Event, Proposal


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
