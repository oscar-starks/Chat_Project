from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

class LoginSerializer(EmailSerializer, PasswordSerializer):
    pass

class UserProfileSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()
    gender = serializers.CharField()
    birth_date = serializers.DateField()