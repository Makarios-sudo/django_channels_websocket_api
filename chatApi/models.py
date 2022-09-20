from django.db import models
import uuid
from django.db import models

from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="recipient")
    body = models.CharField(max_length=200, blank=True)
    is_read_receipt = models.BooleanField(default=False)
    time_sent = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ["-time_sent"]
    
    def __str__(self):
        return f"{self.sender} sent a message to {self.receiver} on {self.time_sent} "


