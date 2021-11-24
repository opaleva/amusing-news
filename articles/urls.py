from django.urls import path
from django.views.decorators.cache import cache_page
from . import views
from .feeds import LatestArticlesFeed

app_name = 'articles'

urlpatterns = [
    path('', cache_page(5)(views.ArticleListView.as_view()), name='index'),
    path('articles/<str:article_slug>', cache_page(5)(views.ArticleView.as_view()), name='article'),
    path('tag/<slug:slug>/', views.ArticleTaggedView.as_view(), name='articles_by_tag'),
    path('feed/', LatestArticlesFeed(), name='feed'),
    path('search/', views.SearchResultsListView.as_view(), name='search'),
]
