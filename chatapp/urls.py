from django.urls import path

from accounts.socket_middleware import TokenAuthMiddleware
from chatapp.consumers import NotificationConsumer
from chatapp.views import GetChatsView, SendMessageView

urlpatterns = [
    path("send_message/", SendMessageView.as_view()),
    path("chats/<int:page_number>/", GetChatsView.as_view()),
]


websocket_urls = [
    path("ws/notification/", TokenAuthMiddleware(NotificationConsumer.as_asgi())),
]
