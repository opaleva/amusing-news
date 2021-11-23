from django import http
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

import logging

from comments.forms import CommentForm
from .mixins import TagMixin
from .models import Article


logger = logging.getLogger(__name__)


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    template_name = 'articles/article/list.html'


class ArticleView(DetailView):
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'article_slug'
    template_name = 'articles/article/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # id = self.kwargs['id']
        slug = self.kwargs['article_slug']
        article = get_object_or_404(Article, slug=slug)
        comments = article.comments.all()
        paginator = Paginator(comments, 20)
        page = self.request.GET.get('page')
        context['comments'] = paginator.get_page(page)
        context['form'] = CommentForm(self.request.POST or None)
        logger.critical('Article page loaded successfully')
        return context


class ArticleTaggedView(TagMixin, ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 10
    template_name = 'articles/article/list.html'

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get('slug'))


class SearchResultsListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/article/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        result = Article.objects.filter(Q(title__regex=fr'{query}') | Q(content__regex=fr'{query}'))
        if result:
            if len(query) < 3:
                return ["Слово для поиска не должно быть короче 3 символов"]
            return result
        else:
            return ["Ничего не найдено"]
