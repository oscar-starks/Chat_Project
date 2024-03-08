from chatapp.threads import MessageImageSaverThread
from chatapp.models import MessageModel
from chatapp.notifications import message_notification

async def messenger(serializer, user,chat):
    image = serializer.validated_data.pop("image", None)
    text = serializer.validated_data.pop("text", None)

    message = await MessageModel.objects.acreate(sender=user)

    if text:
        message.text = text
    if image:
        MessageImageSaverThread(user,message, image, chat).start()
        return str(chat.id)

    else:
        await message.asave()
        await chat.messages.aadd(message)
        await message_notification(user, chat, message)
        return str(chat.id)
