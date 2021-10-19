from django.views.generic import ListView, DetailView

from .models import Article, Comment
from .forms import CommentForm


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 10
    template_name = 'articles/article/list.html'

    def get_queryset(self):
        return Article.published.all()


class ArticleView(DetailView):
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'article'
    template_name = 'articles/article/detail.html'


# class CommentCreate