from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from accounts.models import User
from accounts.responses import CustomErrorResponse, CustomSuccessResponse
from chatapp.chat_message import messenger
from chatapp.models import Chat, MessageModel
from chatapp.notifications import read_receipt_notification
from chatapp.serializers import (
    AudioSerializer,
    ChatSerializer,
    GetMessagesSerializer,
    MessageSerializer,
    SendMessageSerializer,
)
from chatapp.threads import MessageImageSaverThread
from common.custom_authentications import IsAuthenticatedCustom
from common.paginator import customPaginator
