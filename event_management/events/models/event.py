import uuid

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
