from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles'),
    path('<pk>/<slug:article>', views.ArticleView.as_view(), name='article'),
    path('tag/<slug:tag_slug>/', views.ArticleListView.as_view(), name='articles_by_tag'),
]
