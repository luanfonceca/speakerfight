from django import template

register = template.Library()


@register.filter
def already_voted(user, proposal):
    return proposal.user_already_votted(user)


@register.filter
def allowed_to_vote(user, proposal):
    return proposal.user_can_vote(user)


@register.filter
def get_rate_display(user, proposal):
    return proposal.votes.get(user=user).get_rate_display()
