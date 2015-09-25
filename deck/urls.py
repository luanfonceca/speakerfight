from django.conf.urls import patterns

from smarturls import surl as url

import views

urlpatterns = patterns(
    '',
    url(regex=r'/my_proposals/',
        view=views.ListMyProposals.as_view(),
        name='my_proposals'),
    url(regex=r'/events/',
        view=views.ListEvents.as_view(),
        name='list_events'),
    url(regex=r'/events/create/',
        view=views.CreateEvent.as_view(),
        name='create_event'),
    url(regex=r'/events/<slug:slug>/',
        view=views.DetailEvent.as_view(),
        name='view_event'),
    url(regex=r'/events/<slug:slug>/update/',
        view=views.UpdateEvent.as_view(),
        name='update_event'),
    url(regex=r'/events/<slug:slug>/export/',
        view=views.ExportEvent.as_view(),
        name='export_event'),
    url(regex=r'/events/<slug:slug>/create_schedule/',
        view=views.CreateEventSchedule.as_view(),
        name='create_event_schedule'),
    url(regex=r'/events/<slug:slug>/proposals/create/',
        view=views.CreateProposal.as_view(),
        name='create_event_proposal'),
    url(regex=r'/events/<slug:slug>/schedule/',
        view=views.DetailEventSchedule.as_view(),
        name='view_event_schedule'),
    url(regex=r'/events/<slug:event_slug>/'
              r'proposals/<slug:slug>/update/',
        view=views.UpdateProposal.as_view(),
        name='update_proposal'),
    url(regex=r'/events/<slug:event_slug>/'
              r'proposals/<slug:slug>/delete/',
        view=views.DeleteProposal.as_view(),
        name='delete_proposal'),
    url(regex=r'/events/<slug:event_slug>/'
              r'proposals/<slug:slug>/rate/<slug:rate>/',
        view=views.RateProposal.as_view(),
        name='rate_proposal'),
    url(regex=r'/events/<slug:event_slug>/'
              r'proposals/<slug:slug>/approve_proposal/',
        view=views.ApproveProposal.as_view(),
        name='approve_proposal'),
    url(regex=r'/events/<slug:event_slug>/'
              r'proposals/<slug:slug>/disapprove_proposal/',
        view=views.DisapproveProposal.as_view(),
        name='disapprove_proposal'),
)
