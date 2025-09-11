from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


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

    await channel_layer.group_send(
        f"{user.uuid}__notifications",
        {"type": "notification", "message": notification_data},
    )


async def read_receipt_notification(user, message_id, chat_id):
    """
    This function is called when a new message is opened.
    It returns the ID of the message that was received
    showing that it has been read
    """

    notification_data = {
        "notification_type": "read_receipt",
        "notification_data": {"chat_id": str(chat_id), "message_id": message_id},
    }

    await channel_layer.group_send(
        f"{user.uuid}__notifications",
        {"type": "notification", "message": notification_data},
    )
