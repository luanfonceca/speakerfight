try:
    from django.views.i18n import JavaScriptCatalog

    javascript_catalog = JavaScriptCatalog.as_view()
except:
    from django.views.i18n import javascript_catalog

from smarturls import surl as url

from . import views

urlpatterns = (
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
    url(regex=r'/profile/<username:user__username>/update/picture/',
        view=views.ProfileUpdatePictureView.as_view(),
        name='update_profile_picture'),
    url(r'^jsi18n/$', javascript_catalog, name='javascript_catalog'),
    url(regex=r'/profile/<username:user__username>/change/language/',
        view=views.ProfileChangeLanguageView.as_view(),
        name='change_language'),
    url(r'^jsi18n/$', javascript_catalog, name='javascript-catalog'),
)
