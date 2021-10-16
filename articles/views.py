from django.shortcuts import render, get_object_or_404
from .models import Article


def articles_list(request):
    articles = Article.published.all()
    return render(request, 'articles/article/list.html', {'articles': articles})


def article_detail(request, year, month, day, article):
    article = get_object_or_404(Article, slug=article,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    return render(request, 'articles/article/detail.html', {'article': article})
