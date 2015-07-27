from django.conf.urls import url

from api.views import ListProposalView


urlpatterns = [
    url(u'^events/(?P<slug>.+)/proposals/$', ListProposalView.as_view()),
]
