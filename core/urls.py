from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.i18n import javascript_catalog

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name="index.html"),
        name='index_page'),
    url(r'^jsi18n/$', javascript_catalog, name='javascript_catalog'),
)
