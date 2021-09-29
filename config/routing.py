from config.settings import ASGI_APPLICATION
from .asgi import *
from .wsgi import *
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

ASGI_APPLICATION = "config.routing.application"

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))}
)
