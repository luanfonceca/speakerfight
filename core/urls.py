from django.conf.urls import patterns, url
from django.views.i18n import javascript_catalog

from core import views

from smarturls import surl as url


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(),
        name='index_page'),
    url(regex=r'/profile/',
        view=views.ProfileView.as_view(),
        name='profile'),
    url(regex=r'/about/',
        view=views.AboutView.as_view(),
        name='about'),
    url(regex=r'/profile/<username:user__username>/',
        view=views.ProfileView.as_view(),
        name='user_profile'),
    url(regex=r'/profile/<username:user__username>/update/',
        view=views.ProfileUpdateView.as_view(),
        name='update_profile'),
    url(r'^jsi18n/$', javascript_catalog, name='javascript_catalog'),
    url(r'/feedback/', views.FeedbackView.as_view(), name='feedback'),
)
