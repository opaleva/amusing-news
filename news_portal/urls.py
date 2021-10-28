"""news_portal URL Configuration"""
# from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

import debug_toolbar

from articles.sitemaps import ArticleSitemap

sitemaps = {
    'articles': ArticleSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('__debug__/', include(debug_toolbar.urls)),
]

# urlpatterns = i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('', include('articles.urls')),
#     path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
#          name='django.contrib.sitemaps.views.sitemap'),
#     path('__debug__/', include(debug_toolbar.urls)),
# )

