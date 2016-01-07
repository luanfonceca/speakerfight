from django.conf.urls import patterns
from django.views.i18n import javascript_catalog

from smarturls import surl as url

from core import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(),
        name='index_page'),
    url(regex=r'/profile/',
        view=views.ProfileView.as_view(),
        name='profile'),
    url(regex=r'/profile/<slug:user__username>/',
        view=views.ProfileView.as_view(),
        name='profile'),
    url(regex=r'/profile/<slug:user__username>/update/',
        view=views.ProfileUpdateView.as_view(),
        name='update_profile'),
    url(r'^jsi18n/$', javascript_catalog, name='javascript_catalog'),
)
