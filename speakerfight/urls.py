from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from vanilla import TemplateView


urlpatterns = (
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^', include('core.urls')),
    url(r'^', include('deck.urls')),
    url(r'^', include('jury.urls')),
    url(r'^organizations/', include('organization.urls')),
    url(r'^api/', include('api.urls')),
)

urlpatterns += tuple(
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += (
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )

handler500 = TemplateView.as_view(template_name='500.html')
