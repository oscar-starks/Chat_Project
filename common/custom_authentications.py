import json

from asgiref.sync import sync_to_async
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

from common.custom_functions import decodeJWT


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        if not http_auth:
            raise AuthenticationFailed("Auth token not provided!")
        try:
            user = decodeJWT(http_auth)
        except:
            raise AuthenticationFailed("Auth token invalid or expired!")

        if not user:
            raise AuthenticationFailed("Auth token invalid or expired!")
        request.user = user
        if request.user and request.user.is_authenticated:
            # user = User.objects.get(id=request.user.id)
            user.last_login = timezone.now()
            user.save()

            return True
        return False


async def authenticate(self, callback=None):
    """
    this takes the default argument of self and an optional callback. the callback
    is a function that will be called if you want to perform the authentication
    yourself.
    """

    self.user = self.scope["user"]

    if self.user is not None:
        id = await sync_to_async(getattr)(self.user, "uuid")
        self.room_group_name = f"{id}__notifications"

        if callback is not None:
            response = await callback(self)

            await self.send(
                text_data=json.dumps(
                    {"type": response["status"], "message": response["message"]}
                )
            )

            if not response["connection_status"]:
                await self.close(code=1000)

        else:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            await self.accept()

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "connection established",
                        "message": "connection successful",
                    }
                )
            )
    else:
        await self.accept()
        await self.send(
            text_data=json.dumps(
                {"type": "connection rejected", "message": "authentication failed"}
            )
        )
        await self.close(code=1000)
