from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, ListView, DetailView


admin.autodiscover()

urlpatterns = [
    url(r'^', include('status.urls', namespace='status', app_name='status')),
    url(r'^account/login/$', login, {'template_name': 'admin/login.html'}, 'login'),
    url(r'^account/logout/$', logout, {'template_name': 'admin/logout.html'}, 'logout'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]

# if settings.DEBUG:
#     urlpatterns += url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#         'document_root': settings.MEDIA_ROOT,
#     }),
#     urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
