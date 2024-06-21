import json

import jwt
from asgiref.sync import sync_to_async
from django.conf import settings

from accounts.models import User


def decodeJWTForSocket(bearer):
    if not bearer:
        return None

    try:
        decoded = jwt.decode(bearer, settings.SECRET_KEY, algorithms=["HS256"])
    except:
        return None

    if decoded:
        try:
            user = User.objects.get(uuid=decoded["user_id"])
            return user
        except Exception:
            return None


async def authenticate(self, callback=None):
    self.user = self.scope["user"]

    if self.user is not None:
        id = await sync_to_async(getattr)(self.user, "uuid")
        self.room_group_name = f"{id}__notifications"

        if callback is not None:
            response = await callback(self)

            if response is not None and "message" in response:
                await self.accept()

                await self.send(
                    text_data=json.dumps(
                        {"type": response["status"], "message": response["message"]}
                    )
                )

                await self.close(code=1000)

            else:
                if response is not None and "extra_data" in response:
                    for key in response["extra_data"].keys():
                        await sync_to_async(setattr)(
                            self, key, response["extra_data"][key]
                        )

                await self.channel_layer.group_add(
                    self.room_group_name, self.channel_name
                )

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
