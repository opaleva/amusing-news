"""news_portal URL Configuration"""
# from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

import debug_toolbar

from news_portal import settings
from articles.sitemaps import ArticleSitemap


sitemaps = {
    'articles': ArticleSitemap
}

urlpatterns = [
    path('veryimportantpage/', admin.site.urls),
    path('comments/', include('comments.urls', namespace='comments')),
    path("users/", include("users.urls")),
    path("users/", include("django.contrib.auth.urls")),
    path('', include('articles.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('', include('articles.urls')),
#     path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
#          name='django.contrib.sitemaps.views.sitemap'),
#     path('__debug__/', include(debug_toolbar.urls)),
# )

