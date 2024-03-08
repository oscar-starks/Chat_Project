import uuid
from django.db import models


class TimeStampedUUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
