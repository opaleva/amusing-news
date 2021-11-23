from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.utils.feedgenerator import Atom1Feed

from .models import Article


class LatestArticlesFeed(Feed):
    title = 'Несерьёзные новости'
    link = reverse_lazy('articles:index')
    description = 'Новые несерьёзные новости'
    feed_type = Atom1Feed

    def items(self):
        return Article.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
