from rest_framework import serializers
from accounts.serializers import UserProfileSerializer
from django.core.validators import FileExtensionValidator
from chatapp.notifications import read_receipt_notification
from chatapp.models import Chat
from asgiref.sync import async_to_sync



class SendMessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    receiver_id = serializers.UUIDField(write_only= True)
    voice_note = serializers.FileField(validators=[
                        FileExtensionValidator(allowed_extensions=['mp3', 'wav'])
                        ], required = False)


    def validate(self, data):
        if not data.get("text") and not data.get("image") and not data.get("voice_note"):
            raise serializers.ValidationError(
                    {
                    "status": "error",
                    "message": "You must enter a text or an image or a voice_note."
                    }
            )
        
        return data

class MessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    receiver_id = serializers.UUIDField(write_only= True)
    created_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.SerializerMethodField(read_only=True)
    voice_note = serializers.FileField(validators=[
                        FileExtensionValidator(allowed_extensions=['mp3', 'wav'])
                        ], required = False)
    is_read = serializers.BooleanField(read_only=True)
    id = serializers.UUIDField(read_only = True)
    

    def __init__(self, queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = self.context
        request = context["request"]

        print(queryset[0].sender.email)
        print(request.user.email)
        for i in queryset:
            print(i.sender.email, "--------------------------------")
        
        if queryset is not None and not queryset[0].is_read and request.user != queryset[0].sender:
            message = queryset[0]
            chat = Chat.objects.get(messages = message)
            message_id = [str(i.id) for i in queryset]
            
            async_to_sync(read_receipt_notification)(message.sender, message_id, chat.id)

            for instance in queryset:
                instance.is_read = True
                instance.save()
                instance.is_read = False


    def validate(self, data):
        if not data.get("text") and not data.get("image") and not data.get("voice_note"):
            raise serializers.ValidationError(
                    {
                    "status": "error",
                    "message": "You must enter a text or an image or a voice_note."
                    }
            )
        
        return data
    
    def to_representation(self, instance):
        data = super(MessageSerializer, self).to_representation(instance)
        print(instance)
        return data
    
    

    def get_user_id(self, message):
        return str(message.sender.uuid)
   

class ChatSerializer(serializers.Serializer):
    user1 = UserProfileSerializer(many =False)
    user2 = UserProfileSerializer(many = False)
    created_at = serializers.DateTimeField(read_only=True)
    id = serializers.CharField()


    def to_representation(self, instance):
        data = super(ChatSerializer, self).to_representation(instance)
        data["user1"].pop("birth_date", None)
        data["user2"].pop("birth_date", None)

        return data
    

class GetMessagesSerializer(serializers.Serializer):
    chat_id = serializers.CharField()


class AudioSerializer(serializers.Serializer):
    audio = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])])
    receiver_id = serializers.UUIDField()
