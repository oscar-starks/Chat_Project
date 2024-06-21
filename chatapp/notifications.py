import json

import websockets
from asgiref.sync import sync_to_async
from decouple import config

from common.custom_functions import get_socket_access_token


async def message_notification(user, chat, message):
    chat_id = await sync_to_async(getattr)(chat, "id")

    notification_data = {
        "notification_type": "new_message",
        "notification_data": {
            "chat_id": str(chat_id),
            "sender_name": message.sender.full_name,
            "user_id": str(user.uuid),
            "text": message.text,
            "image": message.image_url,
            "date_time": str(message.created_at),
            "message_id": str(message.id),
        },
    }

    HOST = config("HOST")

    access = get_socket_access_token({"user_id": (str(user.uuid))})

    uri = f"ws://{HOST}/ws/notification/"

    async with websockets.connect(uri, extra_headers={"token": access}) as websocket:
        await websocket.send(json.dumps({"data": notification_data}))


async def read_receipt_notification(user, message_id, chat_id):
    """
    This function is called when a new message is opened.
    It returns the ID of the message that was received
    showing that it has been read
    """

    access = get_socket_access_token({"user_id": (str(user.uuid))})
    HOST = config("HOST")
    uri = f"ws://{HOST}/ws/notification/"

    notification_data = {
        "notification_type": "read_receipt",
        "notification_data": {"chat_id": str(chat_id), "message_id": message_id},
    }

    async with websockets.connect(uri, extra_headers={"token": access}) as websocket:
        await websocket.send(json.dumps({"data": notification_data}))
