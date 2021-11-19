from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, ListView, DetailView


admin.autodiscover()

urlpatterns = [
    path('', include('status.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('avatar/', include('avatar.urls')),
    path('admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
