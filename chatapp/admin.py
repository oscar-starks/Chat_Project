from django.contrib import admin
from chatapp.models import MessageModel, Chat

admin.site.register(MessageModel)
admin.site.register(Chat)
