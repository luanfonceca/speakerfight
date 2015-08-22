from smarturls import surl as url

from api import views


urlpatterns = [
    url(
        r'/events/<slug:slug>/',
        views.RetrieveEventView.as_view(),
        name='api_view_event_grade'
    ),
    url(
        r'/events/<slug:slug>/activities/',
        views.CreateActivityView.as_view(),
        name='api_event_create_activity'
    ),
    url(
        r'/events/<slug:event_slug>/activities/<slug:slug>/',
        views.ActivityView.as_view(),
        name='api_event_activity'
    ),
]
