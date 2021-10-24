from django import template
from django.db.models import Count
from django.shortcuts import get_object_or_404

from ..models import Article

register = template.Library()


@register.simple_tag(name='numbers')
def total_articles():
    return Article.published.count()


@register.simple_tag
def get_popular(count=5):
    return Article.published.annotate(
        all_comments=Count('comments')
    ).order_by('-all_comments')[:count]
