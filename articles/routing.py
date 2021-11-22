from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'/(?P<article_id>\d+)/', consumers.CommentsConsumer.as_asgi())
    # path("ws/articles/<pk>/<slug:article>/", consumers.CommentsConsumer.as_asgi())
]
