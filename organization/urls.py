
from smarturls import surl as url

from . import views

urlpatterns = (
    url(regex=r'/create/',
        view=views.CreateOrganization.as_view(),
        name='create_organization'),
    url(regex=r'/<slug:slug>/update/',
        view=views.UpdateOrganization.as_view(),
        name='update_organization'),
    url(regex=r'/<slug:slug>/delete/',
        view=views.DeleteOrganization.as_view(),
        name='delete_organization'),
)
