from config.settings import ASGI_APPLICATION
from .asgi import *
from .wsgi import *
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

<<<<<<< HEAD
# ASGI_APPLICATION="config.routing.application"
=======
ASGI_APPLICATION = "config.routing.application"
>>>>>>> 41e547da9de11c963a2b35eed6aafd683537d30a

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))}
)
