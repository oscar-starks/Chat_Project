import threading, asyncio, requests
from io import BytesIO
from chatapp.notifications import message_notification
from django.dispatch import receiver
from django.db.models.signals import pre_save
from chatapp.models import MessageModel


class MessageImageSaverThread(threading.Thread): 
    def __init__(self, user, obj, image, chat):
        self.obj = obj
        self.image = image
        self.chat = chat
        self.user = user

        # I'm making these attributes globally accessible
        # so it can be accessed by the signal that's declared
        # down on line 62
        global chat_variable
        global message_variable
        global user_variable

        user_variable = self.user
        chat_variable = self.chat
        message_variable = self.obj

        threading.Thread.__init__(self)

    def run(self):
        image_file = BytesIO(self.image.read())
        self.obj.image.save(self.image.name, image_file)
        self.chat.messages.add(self.obj)


# I had to create  this signal to send messages to users when
# the image has been saved on aws so that the image url can be obtained

@receiver(pre_save, sender=MessageModel)
def message_notification_signal(sender, instance, **kwargs):
    if instance.image_url:
        asyncio.run(message_notification(user_variable, chat_variable, message_variable))


