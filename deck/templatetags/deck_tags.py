from django import template

register = template.Library()


@register.filter
def already_voted(user, proposal):
    return proposal.user_already_votted(user)


@register.filter
def allowed_to_vote(user, proposal):
    if user.is_superuser:
        return True
    if not proposal.event.allow_public_voting:
        return False
    if not user.is_authenticated():
        return True
    if proposal.author_id == user.pk:
        return False
    if already_voted(user, proposal):
        return False
    if proposal.event.jury.users.filter(pk=user.pk).exists():
        return True
