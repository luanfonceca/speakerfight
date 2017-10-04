
from smarturls import surl as url

from . import views

urlpatterns = (
    url(regex=r'/organizations/create/',
        view=views.CreateOrganization.as_view(),
        name='create_organization'),
    url(regex=r'/organizations/<slug:slug>/update/',
        view=views.UpdateOrganization.as_view(),
        name='update_organization'),
)
