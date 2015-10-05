from django.conf.urls import patterns, url
from django.views.i18n import javascript_catalog

from core.views import IndexView

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(),
        name='index_page'),
    url(r'^jsi18n/$', javascript_catalog, name='javascript_catalog'),
)
