from asgiref.sync import sync_to_async
from common.custom_functions import get_socket_access_token
from decouple import config
import json, websockets


async def message_notification(user, chat, message):
    chat_id = await sync_to_async(getattr)(chat, "id")

    notification_data = {
        "notification_type": "new_message",
        "notification_data": {
            "chat_id": str(chat_id),
            "sender_name":message.sender.full_name,
            "user_id": str(user.uuid),
            "text": message.text,
            "image": message.image_url,
            "date_time": str(message.created_at),
            "message_id": str(message.id)
            }
        }
    
    HOST = config("HOST")

    access = get_socket_access_token({"user_id": (str(user.uuid))})

    uri = f"ws://{HOST}/ws/notification/"

    async with websockets.connect(uri, extra_headers={"token":access}) as websocket:
        await websocket.send(json.dumps({"data":notification_data}))

