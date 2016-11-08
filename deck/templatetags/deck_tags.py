import hashlib

from django.contrib.auth.models import AnonymousUser
from django import template
register = template.Library()

from deck.models import Vote


@register.filter
def already_voted(user, proposal):
    return proposal.user_already_voted(user)


@register.filter
def allowed_to_vote(user, proposal):
    return proposal.user_can_vote(user)


@register.filter
def get_rate_display(user, proposal):
    if user.is_authenticated():
        vote = proposal.votes.filter(user=user)
        if vote:
            return vote.first().get_rate_display()


@register.filter
def get_rate_title(rate):
    return Vote.VOTE_TITLES.get(rate)


@register.filter
def get_user_photo(user, size=40):
    social = user.socialaccount_set.first()

    if social:
        return social.get_avatar_url()

    return 'http://www.gravatar.com/avatar/{}?s={}&d=mm'.format(
        hashlib.md5(user.email).hexdigest(), size)


@register.filter
def is_user_in_jury(event, user):
    if isinstance(user, AnonymousUser):
        return False
    return event.jury.users.filter(pk=user.pk).exists()


@register.filter
def event_get_embedded_code(schedule_url):
    iframe_resizer = ('https://cdn.rawgit.com/davidjbradshaw/'
                      'iframe-resizer/master/js/iframeResizer.min.js')
    return (
        '<iframe src="{schedule_url}" frameborder="0" width="100%" '
        'vspace="0" hspace="0" marginheight="5" marginwidth="5" '
        'scrolling="auto" allowtransparency="true" kwframeid="1"></iframe>'
        '<script type="text/javascript" src="{iframe_resizer}"></script>'
        '<script type="text/javascript">iFrameResize()</script>'
    ).format(schedule_url=schedule_url, iframe_resizer=iframe_resizer)
