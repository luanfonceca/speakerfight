from django.contrib import auth

from rest_framework import serializers

from deck.models import Proposal
from deck.templatetags.deck_tags import get_user_photo


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_full_name(self, user):
        return user.get_full_name()

    def get_photo(self, user):
        return get_user_photo(user)

    class Meta:
        model = auth.get_user_model()
        fields = ('full_name', 'photo')


class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Proposal
        fields = ('title', 'description', 'author')
