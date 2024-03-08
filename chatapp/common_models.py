import uuid
from django.db import models
from django.utils import timezone

class TimeStampedUUIDModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    created_at = models.DateTimeField(default = timezone.now)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
