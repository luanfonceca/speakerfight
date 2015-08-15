from django.conf.urls import url

from api.views import RetrieveEventView


urlpatterns = [
    url(
        u'^events/(?P<slug>.+)/$',
        RetrieveEventView.as_view(),
        name='api_view_event_grade'
    ),
]
