from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles'),
    path('<int:year>/<int:month>/<int:day>/<slug:article>', views.ArticleView.as_view(), name='article'),
]
