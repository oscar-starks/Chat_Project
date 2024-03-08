from rest_framework.views import APIView
from accounts.responses import CustomErrorResponse, CustomSuccessResponse
from common.custom_authentications import IsAuthenticatedCustom
from chatapp.serializers import MessageSerializer
from django.db.models import Q
from chatapp.models import Chat, MessageModel
from chatapp.threads import MessageImageSaverThread
from chatapp.chat_message import messenger
from accounts.models import User
from chatapp.serializers import ChatSerializer, MessageSerializer, GetMessagesSerializer, AudioSerializer
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from common.paginator import customPaginator
from adrf.views import APIView as AsyncAPIView
