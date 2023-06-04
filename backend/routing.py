from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from .urls import websocket_patterns
application = ProtocolTypeRouter({
    # (http -> django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_patterns
        )
    )
})