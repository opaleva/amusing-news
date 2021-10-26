from django.urls import path
from . import views
from .feeds import LatestArticlesFeed


app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles'),
    path('<pk>/<slug:article>', views.ArticleView.as_view(), name='article'),
    path('tag/<slug:slug>/', views.ArticleTaggedView.as_view(), name='articles_by_tag'),
    path('feed/', LatestArticlesFeed(), name='feed'),
    path('search/', views.SearchResultsListView.as_view(), name='search'),
]
