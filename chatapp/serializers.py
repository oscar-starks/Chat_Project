from rest_framework import serializers
from accounts.serializers import UserProfileSerializer
from django.core.validators import FileExtensionValidator

class MessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    receiver_id = serializers.UUIDField(write_only= True)
    created_at = serializers.DateTimeField(read_only=True)
    user_id = serializers.SerializerMethodField(read_only=True)
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
        
        if data.get("voice_note"):
            voice_note = data.get("voice_note")

            print(voice_note.size)
        
        return data

    def get_user_id(self, message):
        return str(message.sender.id)
   

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
