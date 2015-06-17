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
    return proposal.votes.get(user=user).get_rate_display()


@register.filter
def get_rate_title(rate):
    return Vote.VOTE_TITLES.get(rate)


@register.filter
def get_user_photo(user):
    social = user.socialaccount_set.first()

    if social:
        return social.get_avatar_url()

    return 'http://www.gravatar.com/avatar/{}'.format(
        hashlib.md5(user.email).hexdigest())


@register.filter
def is_user_in_jury(event, user):
    if isinstance(user, AnonymousUser):
        return False
    return event.jury.users.filter(pk=user.pk).exists()
