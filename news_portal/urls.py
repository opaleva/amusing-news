"""news_portal URL Configuration"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

import debug_toolbar

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
)
