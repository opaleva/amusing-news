from django import http
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .mixins import TagMixin
from .models import Article
from .forms import CommentForm


class ArticleListView(ListView):
    model = Article
    paginate_by = 10
    template_name = 'articles/article/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        context['comments'] = comments
        context['form'] = form
        context['article'] = article
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super(ArticleView, self).get_context_data(**kwargs)
        article = Article.objects.filter(id=self.kwargs['pk'])[0]
        comments = article.comments.all()

        context['comments'] = comments
        context['form'] = form
        context['article'] = article

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            new_comment = CommentForm()
            context['new_comment'] = new_comment
            return http.HttpResponseRedirect('')

        return self.render_to_response(context=context)


class ArticleTaggedView(TagMixin, ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 10
    template_name = 'articles/article/list.html'

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get('slug'))
