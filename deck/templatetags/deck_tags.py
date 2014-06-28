from django import template

register = template.Library()


@register.filter
def allowed_to_vote(user, proposal):
    return (not proposal.user_already_votted(user) and
            proposal.event.allow_public_voting and
            not proposal.author_id == user.id)


@register.filter
def already_voted(user, proposal):
    return proposal.user_already_votted(user)
