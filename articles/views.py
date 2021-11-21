from django import http
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

import logging

from .mixins import TagMixin
from .models import Article
from .forms import CommentForm


logger = logging.getLogger(__name__)


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'articles/article/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.warning('Start page loaded successfully')
        context['articles'] = Article.published.all()
        return context


class ArticleView(DetailView):
    model = Article
    slug_url_kwarg = 'article'
    template_name = 'articles/article/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        slug = self.kwargs['article']
        form = CommentForm()
        article = get_object_or_404(Article, pk=pk, slug=slug)
        comments = article.comments.all()
        paginator = Paginator(comments, 20)
        page = self.request.GET.get('page')

        context['comments'] = paginator.get_page(page)
        context['form'] = form
        context['article'] = article
        logger.critical('Article page loaded successfully')
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super(ArticleView, self).get_context_data(**kwargs)
        article = Article.objects.filter(id=self.kwargs['pk'])[0]

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            new_comment = CommentForm()
            context['new_comment'] = new_comment
            logger.warning('Comment has been added')
            return http.HttpResponseRedirect('')

        return self.render_to_response(context=context)


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
        result = Article.objects.filter(Q(title__regex=fr'{query}') | Q(body__regex=fr'{query}'))
        if result:
            if len(query) < 3:
                return ["Слово для поиска не должно быть короче 3 символов"]
            return result
        else:
            return ["Ничего не найдено"]
