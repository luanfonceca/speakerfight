from rest_framework import generics, permissions

from django.shortcuts import get_object_or_404

from api import serializers
from deck.models import Event, Activity
from deck.forms import ActivityForm, ActivityTimetableForm


class IsJuryPermission(permissions.BasePermission):
    message = 'You are not allowed to see this page.'

    def has_permission(self, request, view):
        slug = view.kwargs.get('event_slug', view.kwargs.get('slug'))
        event = get_object_or_404(Event, slug=slug)
        is_jury = event.jury.users.filter(pk=request.user.pk).exists()
        return is_jury or request.user.is_superuser


class RetrieveEventView(generics.RetrieveAPIView):
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    lookup_field = 'slug'


class CreateActivityView(generics.CreateAPIView):
    serializer_class = serializers.CreateActivitySerializer
    form_class = ActivityForm
    permission_classes = (
        permissions.IsAuthenticated,
        IsJuryPermission,
    )

    def perform_create(self, serializer):
        event = get_object_or_404(Event, slug=self.kwargs.get('slug'))
        serializer.save(
            author=self.request.user,
            track=event.tracks.first()
        )


class ActivityView(generics.RetrieveAPIView,
                   generics.UpdateAPIView,
                   generics.DestroyAPIView):
    serializer_class = serializers.ActivitySerializer
    form_class = ActivityTimetableForm
    queryset = Activity.objects.all()
    lookup_field = 'slug'
    permission_classes = (
        permissions.IsAuthenticated,
        IsJuryPermission,
    )

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(
            queryset,
            track__event__slug=self.kwargs.get('event_slug'),
            slug=self.kwargs.get('slug'))
