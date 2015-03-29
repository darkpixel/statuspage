from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import DetailView, ListView, TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('status.urls', namespace='status', app_name='status')),
    url(r'^account/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, 'login'),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', 'logout'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
