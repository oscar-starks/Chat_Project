from django.contrib import admin

from chatapp.models import Chat, MessageModel

admin.site.register(MessageModel)
admin.site.register(Chat)
