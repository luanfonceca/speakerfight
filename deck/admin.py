from django.contrib import admin

from .models import Event, Proposal, Vote

admin.site.register(Event)
admin.site.register(Proposal)
admin.site.register(Vote)
