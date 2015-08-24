from rest_framework import permissions

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from deck.models import Event


class IsJuryPermission(permissions.BasePermission):
    message = _('You are not allowed to see this page.')

    def has_permission(self, request, view):
        slug = view.kwargs.get('event_slug', view.kwargs.get('slug'))
        event = get_object_or_404(Event, slug=slug)
        return event.jury.users.filter(pk=request.user.pk).exists()


class IsSuperUser(permissions.BasePermission):
    message = _('You are not allowed to see this page.')

    def has_permission(self, request, view):
        return self.request.user.is_superuser


class DeckPermissionMixing(object):
    permission_classes = (
        permissions.IsAuthenticated,
        IsJuryPermission,
        IsSuperUser,
    )
