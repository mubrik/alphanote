from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path('notes/', include('notes.urls')),
    path('notebooks/', include('notebooks.urls')),
    path('admin-page/', admin.site.urls),
    path('accounts/', include('userauth.urls')),
    path('accounts/', include('profiles.urls')),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    re_path(r'^health/', include('health_check.urls')),
    path('', RedirectView.as_view(url='notes/')),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls))) 
