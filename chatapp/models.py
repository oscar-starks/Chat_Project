from django.db import models
from chatapp.common_models import TimeStampedUUIDModel
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class MessageModel(TimeStampedUUIDModel):
    sender = models.ForeignKey(User, related_name="sender_messages", on_delete=models.SET_NULL, null=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(verbose_name=(_("Image")), upload_to="static/chat_images/", null=True, blank=True)
    voice_note = models.FileField(verbose_name=(_("Audio")), upload_to="static/chat_audio/", null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.sender.full_name} : {self.text}"

    class Meta:
        ordering = ["-created_at"]

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = None
        return url
    

class Chat(TimeStampedUUIDModel):
    user1 = models.ForeignKey(User, related_name="user1_chat", on_delete=models.SET_NULL, null=True)
    user2 = models.ForeignKey(User, related_name="user2_chat", on_delete=models.SET_NULL, null=True)
    messages = models.ManyToManyField(MessageModel, blank=True, related_name="chat")

    def __str__(self):
        return f"{self.user1.full_name} - {self.user2.full_name}"

    class Meta:
        verbose_name_plural = "Chat Inboxes"
        ordering = ["-created_at"]
        
