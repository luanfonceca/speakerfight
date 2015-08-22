from django.contrib import auth

from rest_framework.reverse import reverse
from rest_framework import serializers

from deck.models import Event, Activity, Track
from deck.templatetags.deck_tags import get_user_photo


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = auth.get_user_model()
        fields = ('full_name', 'photo')

    def get_full_name(self, user):
        return user.get_full_name() or user.username

    def get_photo(self, user):
        return get_user_photo(user)


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)
    timetable = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            'title', 'slug', 'description', 'timetable',
            'activity_type', 'author',
            'start_timetable', 'end_timetable',
        )

    def get_timetable(self, activity):
        return activity.timetable


class CreateActivitySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    timetable = serializers.SerializerMethodField()
    url_api_event_activity = serializers.SerializerMethodField()
    activity_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            'pk', 'slug', 'title', 'description',
            'timetable', 'activity_type', 'author',
            'start_timetable', 'end_timetable',
            'url_api_event_activity',
            'activity_type_display',
        )

    def get_timetable(self, activity):
        return activity.timetable

    def get_activity_type_display(self, activity):
        return activity.get_activity_type_display()

    def get_url_api_event_activity(self, activity):
        event = activity.track.event
        return reverse(
            'api_event_activity',
            [event.slug, activity.slug])


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    activities = ActivitySerializer(read_only=True, many=True)

    class Meta:
        model = Track
        fields = ('activities',)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    tracks = TrackSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = ('title', 'description', 'tracks')
