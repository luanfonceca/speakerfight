from rest_framework import generics

from api.serializers import EventSerializer
from deck.models import Event


class RetrieveEventView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = 'slug'
