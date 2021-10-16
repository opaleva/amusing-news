from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('', views.articles_list, name='news'),
    path('<int:year>/<int:month>/<int:day>/<slug:article', views.article_detail, name='article'),
]
