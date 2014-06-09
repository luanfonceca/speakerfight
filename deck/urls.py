from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns(
    '',
    url(regex=r'^events/$',
        view=views.ListEvents.as_view(),
        name='list_events'),
    url(regex=r'^events/create/$',
        view=login_required(views.CreateEvent.as_view()),
        name='create_event'),
    url(regex=r'^events/(?P<slug>[-\w\d]+)/$',
        view=views.DetailEvent.as_view(),
        name='view_event'),
    url(regex=r'^events/(?P<slug>[-\w\d]+)/update/$',
        view=login_required(views.UpdateEvent.as_view()),
        name='update_event'),
    url(regex=r'^events/(?P<slug>[-\w\d]+)/proposals/create/$',
        view=login_required(views.CreateProposal.as_view()),
        name='create_event_proposal'),
    url(regex=r'^events/(?P<event_slug>[-\w\d]+)/'
              r'proposals/(?P<slug>[-\w\d]+)/update/$',
        view=login_required(views.UpdateProposal.as_view()),
        name='update_proposal'),
    url(regex=r'^events/(?P<event_slug>[-\w\d]+)/'
              r'proposals/(?P<slug>[-\w\d]+)/rate/(?P<rate>[-\w]+)$',
        view=login_required(views.RateProposal.as_view()),
        name='rate_proposal'),
)
