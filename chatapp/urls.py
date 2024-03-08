from django.urls import path
from chatapp.views import SendMessageView, GetChatsView
from chatapp.consumers import NotificationConsumer
from accounts.socket_middleware import TokenAuthMiddleware


urlpatterns = [
    path("send_message/", SendMessageView.as_view()),
    path("chats/<int:page_number>/", GetChatsView.as_view()),
]


websocket_urls = [
    path("ws/notification/", TokenAuthMiddleware(NotificationConsumer.as_asgi())),
    
]