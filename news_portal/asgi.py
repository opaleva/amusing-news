"""
ASGI config for news_portal project.
"""
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application

import articles.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            articles.routing.websocket_urlpatterns
        )
    )
})
