# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django import template

from django.db.models import Model
from django.template.defaultfilters import urlencode


try:
    from django_bitly.templatetags.bitly import bitlify
    DJANGO_BITLY = True
except ImportError:
    DJANGO_BITLY = False


register = template.Library()


TWITTER_ENDPOINT = 'https://twitter.com/intent/tweet?text=%s'
FACEBOOK_ENDPOINT = 'https://www.facebook.com/sharer/sharer.php?u=%s'
REDDIT_ENDPOINT = 'https://www.reddit.com/submit?url=%s'
TELEGRAM_ENDPOINT = 'https://t.me/share/url?url=%s'
WHATSAPP_ENDPOINT = 'https://api.whatsapp.com/send?text=%s'
VK_ENDPOINT = 'https://vk.com/share.php?url=%s?utm_source=vshare&utm_medium=sharing'


BITLY_REGEX = re.compile(r'^https?://bit\.ly/')


def compile_text(context, text):
    ctx = template.context.Context(context)
    return template.Template(text).render(ctx)


def _build_url(request, obj_or_url):
    if obj_or_url is not None:
        if isinstance(obj_or_url, Model):
            if DJANGO_BITLY:
                url = bitlify(obj_or_url)  # type: str
                if not BITLY_REGEX.match(url):
                    return request.build_absolute_uri(
                        obj_or_url.get_absolute_url()
                    )
                else:
                    return url
            else:
                return request.build_absolute_uri(obj_or_url.get_absolute_url())
        else:
            return request.build_absolute_uri(obj_or_url)
    return ''


def _compose_tweet(text, url=None):
    TWITTER_MAX_NUMBER_OF_CHARACTERS = 140
    TWITTER_LINK_LENGTH = 23  # "A URL of any length will be altered to 23 characters, even if the link itself is less than 23 characters long.

    # Compute length of the tweet
    url_length = len(' ') + TWITTER_LINK_LENGTH if url else 0
    total_length = len(text) + url_length

    # Check that the text respects the max number of characters for a tweet
    if total_length > TWITTER_MAX_NUMBER_OF_CHARACTERS:
        text = text[:(TWITTER_MAX_NUMBER_OF_CHARACTERS - url_length - 1)] + "…"  # len("…") == 1

    return "%s %s" % (text, url) if url else text


@register.simple_tag(takes_context=True)
def post_to_twitter_url(context, obj_or_url=None):
    request = context['request']

    url = _build_url(request, obj_or_url)

    tweet = _compose_tweet(url)
    context['tweet_url'] = TWITTER_ENDPOINT % urlencode(tweet)
    return context


@register.inclusion_tag('twitter.html', takes_context=True)
def post_to_twitter(context, obj_or_url=None, link_text='',link_class=""):
    context = post_to_twitter_url(context, obj_or_url)

    request = context['request']
    url = _build_url(request, obj_or_url)
    tweet = _compose_tweet(url)

    context['link_class'] = link_class
    context['link_text'] = link_text or 'Post to Twitter'
    context['full_text'] = tweet
    return context


@register.simple_tag(takes_context=True)
def post_to_facebook_url(context, obj_or_url=None):
    request = context['request']
    url = _build_url(request, obj_or_url)
    context['facebook_url'] = FACEBOOK_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('fb.html', takes_context=True)
def post_to_facebook(context, obj_or_url=None, link_text='', link_class=''):
    context = post_to_facebook_url(context, obj_or_url)
    context['link_class'] = link_class or ''
    context['link_text'] = link_text or 'Post to Facebook'
    return context


@register.simple_tag(takes_context=True)
def post_to_reddit_url(context, obj_or_url=None):
    request = context['request']
    url = _build_url(request, obj_or_url)
    context['reddit_url'] = REDDIT_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('reddit.html', takes_context=True)
def post_to_reddit(context, obj_or_url=None, link_text='', link_class=''):
    context = post_to_reddit_url(context, obj_or_url)
    context['link_class'] = link_class
    context['link_text'] = link_text or 'Post to Reddit'
    return context


@register.simple_tag(takes_context=True)
def post_to_vk_url(context, obj_or_url=None):
    request = context['request']
    url = _build_url(request, obj_or_url)
    context['vk_url'] = VK_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('vk.html', takes_context=True)
def post_to_vk(context, obj_or_url=None, link_text=''):
    context = post_to_vk_url(context, obj_or_url)
    context['link_text'] = link_text or 'Post to VK'
    return context


@register.simple_tag(takes_context=True)
def post_to_telegram_url(context, obj_or_url=None):
    request = context['request']
    url = _build_url(request, obj_or_url)
    context['telegram_url'] = TELEGRAM_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('tg.html', takes_context=True)
def post_to_telegram(context, obj_or_url=None, link_text='', link_class=''):
    context = post_to_telegram_url(context, obj_or_url)
    context['link_class'] = link_class
    context['link_text'] = link_text or 'Post to Telegram'
    return context


@register.simple_tag(takes_context=True)
def post_to_whatsapp_url(context, obj_or_url=None):
    request = context['request']
    url = _build_url(request, obj_or_url)
    context['whatsapp_url'] = WHATSAPP_ENDPOINT % urlencode(url)
    return context


@register.inclusion_tag('wa.html', takes_context=True)
def post_to_whatsapp(context, obj_or_url=None, link_text='', link_class=''):
    context = post_to_whatsapp_url(context, obj_or_url)
    context['link_class'] = link_class
    context['link_text'] = link_text or 'Post to WhatsApp'
    return context
