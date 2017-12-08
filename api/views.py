import json

from rest_framework import generics
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from api import serializers, permissions
from deck.models import Event, Activity
from deck.forms import ActivityForm, ActivityTimetableForm


class RetrieveEventScheduleView(generics.RetrieveAPIView):
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    lookup_field = 'slug'


class CreateActivityView(permissions.DeckPermissionMixing,
                         generics.CreateAPIView):
    serializer_class = serializers.CreateActivitySerializer
    form_class = ActivityForm

    def perform_create(self, serializer):
        event = get_object_or_404(Event, slug=self.kwargs.get('slug'))
        serializer.save(
            author=self.request.user,
            track=event.tracks.first()
        )


class ActivityView(permissions.DeckPermissionMixing,
                   generics.RetrieveAPIView,
                   generics.UpdateAPIView,
                   generics.DestroyAPIView):
    serializer_class = serializers.ActivitySerializer
    form_class = ActivityTimetableForm
    queryset = Activity.objects.all()
    lookup_field = 'slug'

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(
            queryset,
            track__event__slug=self.kwargs.get('event_slug'),
            slug=self.kwargs.get('slug'))

class UpdateEventScheduleOrderView(permissions.DeckPermissionMixing,
                                   generics.UpdateAPIView):
    queryset = Event.objects.all()
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        activities = json.loads(request.data.get("activities"))
        event = self.get_object()

        for activity in activities:
            Activity.objects.filter(slug=activity['slug']).update(track_order=activity['order'])

        return Response({})
