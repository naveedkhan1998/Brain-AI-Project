# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from django.contrib.staticfiles import views
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from main.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
