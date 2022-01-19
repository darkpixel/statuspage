from django.conf import settings
from django.urls import include, path, re_path, register_converter
from django.contrib import admin
from django.views.generic import TemplateView, ListView, DetailView


admin.autodiscover()

urlpatterns = [
    path('', include('status.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
