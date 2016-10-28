
from smarturls import surl as url

from . import views

urlpatterns = [
    url(regex=r'/events/<slug:slug>/jury/',
        view=views.JuryView.as_view(),
        name='jury_event'),
    url(regex=r'/events/<slug:slug>/invite/jury/',
        view=views.InviteEvent.as_view(),
        name='event_invite_to_jury'),
    url(regex=r'/events/<slug:slug>/remove/jury/<int:user_pk>/',
        view=views.remove_user_from_event_jury,
        name='event_remove_from_jury'),
]
