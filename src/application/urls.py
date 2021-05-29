from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from filebrowser.sites import site as filebrowser_site
from pages.views import Page404View

urlpatterns = [
    url(r'^engine2/admin/', include('public_model.urls')),
    url(r'^engine2/admin/', include(admin.site.urls)),
    url(r'^engine2/admin/admin_tools/', include('admin_tools.urls')),
    url(r'^engine2/admin/filebrowser/', include(filebrowser_site.urls)),
    url(r'^engine2/admin/server_resources/', include('server_resources.urls')),
    url(r'^engine2/admin/cache/', include('cache_model.urls')),
    url(r'^engine2/admin/sort/', include('sort_model.urls')),
    url(r'^', include('application.website.urls')),
    url(r'^shop/', include('application.shop.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]

# Handle static files (only if DEBUG is True)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar
if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

# Page 404
handler404 = Page404View.as_view()
