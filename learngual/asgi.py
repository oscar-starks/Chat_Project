from chatapp.urls import websocket_urls as chatsocketurls
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learngual.settings')

application = ProtocolTypeRouter(
    {'http':get_asgi_application(),
    'websocket':
        URLRouter(
            chatsocketurls
        )
    }
)