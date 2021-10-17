from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Article


def articles_list(request):
    articles_all = Article.published.all()
    paginator = Paginator(articles_all, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'articles/article/list.html',
                  {'page': page, 'articles': articles})


def article_detail(request, year, month, day, article):
    article = get_object_or_404(Article, slug=article,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    return render(request, 'articles/article/detail.html', {'article': article})
